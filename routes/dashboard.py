from flask import Blueprint, render_template, send_file, request, flash, redirect, url_for
from flask_login import login_required
from models.facture import Facture, LigneFacture
from models.client import Client
from models.produit import Produit
from models import db
from datetime import datetime, timedelta
import calendar
import pandas as pd
import io

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Indicateurs principaux
    total_clients = Client.query.count()
    total_factures = Facture.query.count()
    lignes = LigneFacture.query.join(Facture).all()
    total_ht = 0
    total_tva = 0
    total_ttc = 0
    for ligne in lignes:
        if ligne.type_prix == 'HT':
            ligne_ht = ligne.prix * ligne.quantite
            ligne_tva = ligne_ht * ligne.tva / 100
        else:
            ligne_ht = (ligne.prix * ligne.quantite) / (1 + ligne.tva / 100)
            ligne_tva = (ligne.prix * ligne.quantite) - ligne_ht
        total_ht += ligne_ht
        total_tva += ligne_tva
    total_ttc = total_ht + total_tva

    # Chiffre d'affaires TTC par mois (12 derniers mois)
    now = datetime.now()
    ca_mois = []
    mois_labels = []
    for i in range(11, -1, -1):
        mois = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        mois_labels.append(mois.strftime('%b %Y'))
        factures_mois = Facture.query.filter(
            Facture.date >= mois,
            Facture.date < (mois + timedelta(days=32)).replace(day=1)
        ).all()
        ttc_mois = 0
        for f in factures_mois:
            for l in f.lignes:
                if l.type_prix == 'HT':
                    ligne_ht = l.prix * l.quantite
                    ligne_tva = ligne_ht * l.tva / 100
                else:
                    ligne_ht = (l.prix * l.quantite) / (1 + l.tva / 100)
                    ligne_tva = (l.prix * l.quantite) - ligne_ht
                ttc_mois += ligne_ht + ligne_tva
        ca_mois.append(ttc_mois)

    # Top 5 clients par CA TTC
    ca_par_client = {}
    for f in Facture.query.all():
        client = Client.query.get(f.client_id)
        if not client:
            continue
        ttc = 0
        for l in f.lignes:
            if l.type_prix == 'HT':
                ligne_ht = l.prix * l.quantite
                ligne_tva = ligne_ht * l.tva / 100
            else:
                ligne_ht = (l.prix * l.quantite) / (1 + l.tva / 100)
                ligne_tva = (l.prix * l.quantite) - ligne_ht
            ttc += ligne_ht + ligne_tva
        ca_par_client[client.nom_complet] = ca_par_client.get(client.nom_complet, 0) + ttc
    top_clients = sorted(ca_par_client.items(), key=lambda x: x[1], reverse=True)[:5]
    top_clients_labels = [c[0] for c in top_clients]
    top_clients_values = [c[1] for c in top_clients]

    # Histogramme nombre de factures par mois (12 derniers mois)
    factures_par_mois = []
    for i in range(11, -1, -1):
        mois = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        count = Facture.query.filter(
            Facture.date >= mois,
            Facture.date < (mois + timedelta(days=32)).replace(day=1)
        ).count()
        factures_par_mois.append(count)

    # 5 dernières factures
    last_factures = Facture.query.order_by(Facture.date.desc()).limit(5).all()
    last_factures_data = []
    for f in last_factures:
        client = Client.query.get(f.client_id)
        ttc = 0
        for l in f.lignes:
            if l.type_prix == 'HT':
                ligne_ht = l.prix * l.quantite
                ligne_tva = ligne_ht * l.tva / 100
            else:
                ligne_ht = (l.prix * l.quantite) / (1 + l.tva / 100)
                ligne_tva = (l.prix * l.quantite) - ligne_ht
            ttc += ligne_ht + ligne_tva
        last_factures_data.append({
            'client': client.nom_complet if client else 'Client supprimé',
            'date': f.date.strftime('%d/%m/%Y'),
            'ttc': ttc
        })

    # Performance mensuelle
    mois_courant = now.replace(day=1)
    factures_mois_courant = Facture.query.filter(
        Facture.date >= mois_courant,
        Facture.date < (mois_courant + timedelta(days=32)).replace(day=1)
    ).all()
    ca_mois_courant = 0
    for f in factures_mois_courant:
        for l in f.lignes:
            if l.type_prix == 'HT':
                ligne_ht = l.prix * l.quantite
                ligne_tva = ligne_ht * l.tva / 100
            else:
                ligne_ht = (l.prix * l.quantite) / (1 + l.tva / 100)
                ligne_tva = (l.prix * l.quantite) - ligne_ht
            ca_mois_courant += ligne_ht + ligne_tva
    # Moyenne des 3 derniers mois (hors mois courant)
    ca_3mois = []
    for i in range(1, 4):
        mois = (mois_courant - timedelta(days=30*i)).replace(day=1)
        factures_mois = Facture.query.filter(
            Facture.date >= mois,
            Facture.date < (mois + timedelta(days=32)).replace(day=1)
        ).all()
        ttc = 0
        for f in factures_mois:
            for l in f.lignes:
                if l.type_prix == 'HT':
                    ligne_ht = l.prix * l.quantite
                    ligne_tva = ligne_ht * l.tva / 100
                else:
                    ligne_ht = (l.prix * l.quantite) / (1 + l.tva / 100)
                    ligne_tva = (l.prix * l.quantite) - ligne_ht
                ttc += ligne_ht + ligne_tva
        ca_3mois.append(ttc)
    moyenne_3mois = sum(ca_3mois) / 3 if ca_3mois else 0
    performance_score = 0
    if moyenne_3mois > 0:
        performance_score = round((ca_mois_courant - moyenne_3mois) / moyenne_3mois * 100, 1)
    else:
        performance_score = 0

    produits = Produit.query.all()
    clients = Client.query.all()
    return render_template('dashboard.html',
        total_clients=total_clients,
        total_factures=total_factures,
        total_ttc=total_ttc,
        total_ht=total_ht,
        total_tva=total_tva,
        mois_labels=mois_labels,
        ca_mois=ca_mois,
        top_clients_labels=top_clients_labels,
        top_clients_values=top_clients_values,
        factures_par_mois=factures_par_mois,
        last_factures=last_factures_data,
        performance_score=performance_score,
        ca_mois_courant=ca_mois_courant,
        moyenne_3mois=moyenne_3mois,
        produits=produits,
        clients=clients
    )

@dashboard_bp.route('/dashboard/export_excel', methods=['GET', 'POST'])
@login_required
def export_excel():
    # Récupération des filtres
    mois = request.args.get('mois')
    annee = request.args.get('annee')
    jour = request.args.get('jour')
    client_id = request.args.get('client_id')
    produit_id = request.args.get('produit_id')

    query = Facture.query
    if annee:
        query = query.filter(db.extract('year', Facture.date) == int(annee))
    if mois:
        query = query.filter(db.extract('month', Facture.date) == int(mois))
    if jour:
        query = query.filter(db.extract('day', Facture.date) == int(jour))
    if client_id:
        query = query.filter(Facture.client_id == int(client_id))
    factures = query.all()

    data = []
    for f in factures:
        client = Client.query.get(f.client_id)
        for l in f.lignes:
            if produit_id and int(produit_id) != l.produit_id:
                continue
            if l.type_prix == 'HT':
                ligne_ht = l.prix * l.quantite
                ligne_tva = ligne_ht * l.tva / 100
            else:
                ligne_ht = (l.prix * l.quantite) / (1 + l.tva / 100)
                ligne_tva = (l.prix * l.quantite) - ligne_ht
            ligne_ttc = ligne_ht + ligne_tva
            data.append({
                'Facture n°': f.id,
                'Date': f.date.strftime('%d/%m/%Y'),
                'Client': client.nom_complet if client else 'Client supprimé',
                'Produit': l.nom_produit,
                'Quantité': l.quantite,
                'Prix unitaire': l.prix,
                'Type prix': l.type_prix,
                'TVA (%)': l.tva,
                'Montant HT': ligne_ht,
                'Montant TVA': ligne_tva,
                'Montant TTC': ligne_ttc
            })
    if not data:
        flash('Aucune donnée à exporter pour les filtres sélectionnés.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='rapport_factures.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 