from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.parametres import Parametres
from models import db
from models.user import User
import os

parametres_bp = Blueprint('parametres', __name__)

@parametres_bp.route('/parametres', methods=['GET', 'POST'])
@login_required
def parametres():
    cles = ['nom_societe', 'adresse', 'email', 'telephone', 'conditions_paiement', 'logo']
    params = {p.cle: p for p in Parametres.query.filter(Parametres.cle.in_(cles)).all()}
    if request.method == 'POST':
        # Gestion du formulaire paramètres entreprise
        for cle in cles:
            valeur = request.form.get(cle)
            if cle == 'logo' and 'logo' in request.files and request.files['logo'].filename:
                file = request.files['logo']
                filename = 'logo_custom.png'
                filepath = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', filename)
                filepath = os.path.abspath(filepath)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                valeur = filename
            if valeur is not None and valeur != '':
                param = params.get(cle)
                if param:
                    param.valeur = valeur
                else:
                    param = Parametres(cle=cle, valeur=valeur)
                    db.session.add(param)
        # Gestion du formulaire admin
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        if new_username and new_username != current_user.username:
            if User.query.filter_by(username=new_username).first():
                flash('Ce nom d\'utilisateur existe déjà.', 'danger')
                return redirect(url_for('parametres.parametres'))
            current_user.username = new_username
        if new_password:
            current_user.set_password(new_password)
        db.session.commit()
        flash('Paramètres mis à jour.', 'success')
        return redirect(url_for('parametres.parametres'))
    return render_template('parametres.html', params=params)

@parametres_bp.route('/parametres/delete_all', methods=['POST'])
@login_required
def delete_all_data():
    from models.client import Client
    from models.produit import Produit
    from models.facture import Facture, LigneFacture
    from models.parametres import Parametres
    from models.user import User
    from flask_login import logout_user

    password = request.form.get('delete_password')
    if not password or not current_user.check_password(password):
        flash('Mot de passe incorrect.', 'danger')
        return redirect(url_for('parametres.parametres'))

    # Suppression de toutes les données
    LigneFacture.query.delete()
    Facture.query.delete()
    Client.query.delete()
    Produit.query.delete()
    Parametres.query.delete()
    User.query.delete()
    db.session.commit()

    # Recréation de l'admin par défaut
    admin = User(username='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

    logout_user()
    flash('Toutes les données ont été supprimées. Un nouveau compte admin a été créé.', 'success')
    return redirect(url_for('auth.login')) 