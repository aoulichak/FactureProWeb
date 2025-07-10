from flask import Blueprint, render_template, url_for, redirect, flash, request, make_response
from flask_login import login_required
from models.facture import Facture, LigneFacture
from models.client import Client
from models.produit import Produit
from models import db
from datetime import date
from flask import render_template as flask_render_template
import io
from xhtml2pdf import pisa
from models.parametres import Parametres

factures_bp = Blueprint('factures', __name__)

@factures_bp.route('/factures')
@login_required
def factures():
    factures = Facture.query.order_by(Facture.date.desc()).all()
    clients_list = Client.query.all()
    clients = {c.id: c for c in clients_list}
    return render_template('factures.html', factures=factures, clients=clients, clients_list=clients_list)

@factures_bp.route('/factures/add', methods=['GET', 'POST'])
@login_required
def add_facture():
    clients = Client.query.all()
    produits = Produit.query.all()
    if not clients or not produits:
        flash("Veuillez d'abord ajouter au moins un client et un produit.", 'warning')
        return redirect(url_for('factures.factures'))
    if request.method == 'POST':
        client_id = int(request.form['client_id'])
        date_facture = date.today()
        commande_num = request.form.get('commande_num', '')
        facture = Facture(client_id=client_id, date=date_facture, commande_num=commande_num)
        db.session.add(facture)
        db.session.flush()  # pour avoir l'id de la facture
        lignes = []
        for i in range(len(request.form.getlist('produit_id'))):
            produit_id = int(request.form.getlist('produit_id')[i])
            quantite = int(request.form.getlist('quantite')[i])
            prix = float(request.form.getlist('prix')[i])
            type_prix = request.form.getlist('type_prix')[i]
            tva = float(request.form.getlist('tva')[i])
            nom_produit = request.form.getlist('nom_produit')[i]
            if not nom_produit:
                # fallback si le champ caché n'est pas rempli
                produit = Produit.query.get(produit_id)
                nom_produit = produit.nom if produit else ''
            ligne = LigneFacture(
                facture_id=facture.id,
                produit_id=produit_id,
                quantite=quantite,
                prix=prix,
                type_prix=type_prix,
                tva=tva,
                nom_produit=nom_produit
            )
            db.session.add(ligne)
            lignes.append(ligne)
        db.session.commit()
        flash('Facture créée avec succès.', 'success')
        return redirect(url_for('factures.factures'))
    return render_template('facture_form.html', clients=clients, produits=produits, action='add')

@factures_bp.route('/factures/<int:facture_id>')
@login_required
def voir_facture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    client = Client.query.get(facture.client_id)
    lignes = facture.lignes
    return render_template('facture_detail.html', facture=facture, client=client, lignes=lignes)

@factures_bp.route('/factures/delete/<int:facture_id>', methods=['POST'])
@login_required
def delete_facture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    db.session.delete(facture)
    db.session.commit()
    flash('Facture supprimée.', 'success')
    return redirect(url_for('factures.factures'))

@factures_bp.route('/factures/recu/<int:facture_id>')
@login_required
def recu_facture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    client = Client.query.get(facture.client_id)
    lignes = facture.lignes
    total_ht = 0
    total_tva = 0
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
    param = Parametres.query.filter_by(cle='conditions_paiement').first()
    conditions_paiement = param.valeur if param else "<strong>Conditions et modalités de paiement</strong><br>Le paiement est dû dans 15 jours<br><br>Caisse d'Epargne<br>IBAN: FR12 1234 5678<br>SWIFT/BIC: ABCDFRP1XXX"
    # Récupérer tous les paramètres d'entreprise
    cles = ['nom_societe', 'adresse', 'email', 'telephone', 'logo']
    params = {p.cle: p.valeur for p in Parametres.query.filter(Parametres.cle.in_(cles)).all()}
    if not params.get('logo'):
        params['logo'] = 'logo_default.png'
    html = flask_render_template('facture_pdf.html', facture=facture, client=client, lignes=lignes, total_ht=total_ht, total_tva=total_tva, total_ttc=total_ttc, conditions_paiement=conditions_paiement, parametres=params)
    result = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=result, encoding='utf-8')
    response = make_response(result.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=recu_facture_{facture.id}.pdf'
    return response

@factures_bp.route('/factures/edit/<int:facture_id>', methods=['GET', 'POST'])
@login_required
def edit_facture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    clients = Client.query.all()
    produits = Produit.query.all()
    if request.method == 'POST':
        client_id = int(request.form['client_id'])
        commande_num = request.form.get('commande_num', '')
        facture.client_id = client_id
        facture.commande_num = commande_num
        # Supprimer les anciennes lignes
        LigneFacture.query.filter_by(facture_id=facture.id).delete()
        db.session.flush()
        # Ajouter les nouvelles lignes
        for i in range(len(request.form.getlist('produit_id'))):
            produit_id = int(request.form.getlist('produit_id')[i])
            quantite = int(request.form.getlist('quantite')[i])
            prix = float(request.form.getlist('prix')[i])
            type_prix = request.form.getlist('type_prix')[i]
            tva = float(request.form.getlist('tva')[i])
            nom_produit = request.form.getlist('nom_produit')[i]
            if not nom_produit:
                produit = Produit.query.get(produit_id)
                nom_produit = produit.nom if produit else ''
            ligne = LigneFacture(
                facture_id=facture.id,
                produit_id=produit_id,
                quantite=quantite,
                prix=prix,
                type_prix=type_prix,
                tva=tva,
                nom_produit=nom_produit
            )
            db.session.add(ligne)
        db.session.commit()
        flash('Facture modifiée avec succès.', 'success')
        return redirect(url_for('factures.factures'))
    # Préparation des lignes pour pré-remplir le formulaire
    lignes = facture.lignes
    return render_template('facture_form.html', clients=clients, produits=produits, facture=facture, lignes=lignes, action='edit') 