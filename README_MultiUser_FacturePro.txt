FacturePro - Extension Multi-Utilisateurs (Employés)
===================================================

Objectif
--------
Permettre d'ajouter plusieurs utilisateurs (employés) au programme, avec des accès limités selon leur rôle (ex : admin, employé simple).

1. Modèle de données : Ajout des rôles
--------------------------------------
Dans `models/user.py`, ajouter un champ `role` :

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # 'admin' ou 'employee'
    # ...
```

2. Création d'utilisateurs employés
-----------------------------------
Dans l'interface admin (ex : page paramètres), ajouter un formulaire pour créer un nouvel utilisateur :

```python
# routes/parametres.py (extrait)
if request.method == 'POST' and 'new_employee' in request.form:
    username = request.form.get('employee_username')
    password = request.form.get('employee_password')
    if User.query.filter_by(username=username).first():
        flash('Nom d'utilisateur déjà pris.', 'danger')
    else:
        user = User(username=username, role='employee')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Nouvel employé créé.', 'success')
```

3. Gestion des accès limités (décorateur personnalisé)
------------------------------------------------------
Créer un décorateur pour restreindre l'accès à certaines routes :

```python
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Accès réservé à l'administrateur.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
```

Utilisation sur une route :
```python
@app.route('/parametres')
@admin_required
@login_required
def parametres():
    ...
```

4. Exemple d'utilisation dans les templates
-------------------------------------------
Afficher ou masquer des boutons selon le rôle :
```jinja
{% if current_user.role == 'admin' %}
  <a href="{{ url_for('parametres.parametres') }}" class="btn btn-primary">Paramètres</a>
{% endif %}
```

5. Résumé des étapes à suivre
----------------------------
- Ajouter le champ `role` au modèle User (migration nécessaire)
- Adapter les formulaires pour permettre la création d'employés
- Protéger les routes sensibles avec le décorateur `admin_required`
- Adapter les templates pour masquer les actions réservées à l'admin

6. Extensions possibles
----------------------
- Ajouter d'autres rôles (manager, comptable, etc.)
- Gérer les permissions par fonctionnalité (CRUD clients, accès aux rapports, etc.)
- Journaliser les actions des utilisateurs

Cette extension permet de sécuriser l'accès et de déléguer certaines tâches à des employés sans leur donner tous les droits d'administration. 