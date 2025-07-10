from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.produit import Produit
from models import db

produits_bp = Blueprint('produits', __name__)

@produits_bp.route('/produits')
@login_required
def produits():
    produits = Produit.query.all()
    return render_template('produits.html', produits=produits)

@produits_bp.route('/produits/add', methods=['GET', 'POST'])
@login_required
def add_produit():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        prix = float(request.form['prix'])
        type_prix = request.form['type_prix']
        tva = float(request.form['tva'])
        produit = Produit(nom=nom, description=description, prix=prix, type_prix=type_prix, tva=tva)
        db.session.add(produit)
        db.session.commit()
        flash('Produit ajouté avec succès.', 'success')
        return redirect(url_for('produits.produits'))
    return render_template('produit_form.html', action='add')

@produits_bp.route('/produits/edit/<int:produit_id>', methods=['GET', 'POST'])
@login_required
def edit_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    if request.method == 'POST':
        produit.nom = request.form['nom']
        produit.description = request.form['description']
        produit.prix = float(request.form['prix'])
        produit.type_prix = request.form['type_prix']
        produit.tva = float(request.form['tva'])
        db.session.commit()
        flash('Produit modifié avec succès.', 'success')
        return redirect(url_for('produits.produits'))
    return render_template('produit_form.html', produit=produit, action='edit')

@produits_bp.route('/produits/delete/<int:produit_id>', methods=['POST'])
@login_required
def delete_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    db.session.delete(produit)
    db.session.commit()
    flash('Produit supprimé.', 'success')
    return redirect(url_for('produits.produits')) 