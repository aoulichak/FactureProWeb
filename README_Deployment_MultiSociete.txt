FacturePro - Déploiement Multi-Entreprises (SaaS)
=================================================

Objectif
--------
Permettre à chaque entreprise de créer son propre compte sur FacturePro, avec une séparation stricte des données (multi-tenancy/SaaS).

1. Modèle de données : Ajout de la notion de société
----------------------------------------------------
Dans `models/societe.py` (à créer) :
```python
from . import db
class Societe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # ... autres infos société
```
Dans `models/user.py`, lier chaque utilisateur à une société :
```python
class User(UserMixin, db.Model):
    # ...
    societe_id = db.Column(db.Integer, db.ForeignKey('societe.id'), nullable=False)
    societe = db.relationship('Societe', backref='users')
```
Dans les autres modèles (Client, Produit, Facture, etc.), ajouter un champ `societe_id` pour filtrer les données par société.

2. Création de compte société (inscription)
-------------------------------------------
Créer une page d'inscription :
```python
# routes/auth.py
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom_societe = request.form['nom_societe']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        societe = Societe(nom=nom_societe, email=email)
        db.session.add(societe)
        db.session.commit()
        user = User(username=username, societe_id=societe.id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Compte société créé. Connectez-vous.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')
```

3. Séparation stricte des données
---------------------------------
Dans toutes les requêtes (clients, produits, factures...), filtrer par `societe_id` :
```python
# Exemple pour lister les clients de la société courante
clients = Client.query.filter_by(societe_id=current_user.societe_id).all()
```

4. Authentification et session
------------------------------
- À la connexion, l'utilisateur est rattaché à sa société.
- Les templates affichent le nom de la société courante.

5. Déploiement (hébergement)
----------------------------
- Héberger sur un serveur cloud (Heroku, Render, AWS, etc.)
- Configurer la base (PostgreSQL, MySQL, ou Firestore pour le cloud)
- Sécuriser les variables d'environnement (clé secrète, DB URI...)
- Utiliser HTTPS

6. Points d'attention
---------------------
- Sécurité : chaque requête doit être filtrée par `societe_id` pour éviter les fuites de données
- Migration de la base nécessaire (ajout des champs `societe_id`)
- Possibilité d'ajouter des rôles (admin société, employés)
- Gestion des quotas/abonnements (optionnel)

7. Exemple de structure de tables
---------------------------------
- Societe (id, nom, email, ...)
- User (id, username, password_hash, societe_id, ...)
- Client (id, nom_complet, societe_id, ...)
- Produit (id, nom, societe_id, ...)
- Facture (id, client_id, societe_id, ...)

8. Extensions possibles
----------------------
- Personnalisation par société (logo, couleurs, etc.)
- Facturation SaaS (abonnement mensuel)
- Tableau de bord multi-sociétés (pour un super-admin)

Cette architecture permet de transformer FacturePro en une solution SaaS multi-entreprises, sécurisée et évolutive. 