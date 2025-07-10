from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.client import Client
from models import db

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/clients')
@login_required
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@clients_bp.route('/clients/add', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == 'POST':
        nom_complet = request.form['nom_complet']
        entreprise = request.form['entreprise']
        email = request.form['email']
        telephone = request.form['telephone']
        if Client.query.filter_by(email=email).first():
            flash('Cet email existe déjà.', 'danger')
            return redirect(url_for('clients.add_client'))
        client = Client(nom_complet=nom_complet, entreprise=entreprise, email=email, telephone=telephone)
        db.session.add(client)
        db.session.commit()
        flash('Client ajouté avec succès.', 'success')
        return redirect(url_for('clients.clients'))
    return render_template('client_form.html', action='add')

@clients_bp.route('/clients/edit/<int:client_id>', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.nom_complet = request.form['nom_complet']
        client.entreprise = request.form['entreprise']
        client.email = request.form['email']
        client.telephone = request.form['telephone']
        db.session.commit()
        flash('Client modifié avec succès.', 'success')
        return redirect(url_for('clients.clients'))
    return render_template('client_form.html', client=client, action='edit')

@clients_bp.route('/clients/delete/<int:client_id>', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client supprimé.', 'success')
    return redirect(url_for('clients.clients')) 