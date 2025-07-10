import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, redirect, url_for
from models import db
from flask_login import LoginManager, current_user

# Initialisation extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facturepro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Importer User et les blueprints APRÈS l'init
from models.user import User
from models.client import Client
from models.produit import Produit
from models.facture import Facture, LigneFacture
from models.parametres import Parametres
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.clients import clients_bp
from routes.produits import produits_bp
from routes.factures import factures_bp
from routes.parametres import parametres_bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(produits_bp)
app.register_blueprint(factures_bp)
app.register_blueprint(parametres_bp)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    else:
        return redirect(url_for('auth.login'))

@app.context_processor
def inject_parametres():
    cles = ['nom_societe', 'adresse', 'email', 'telephone', 'logo']
    params = {p.cle: p.valeur for p in Parametres.query.filter(Parametres.cle.in_(cles)).all()}
    # Valeur par défaut pour le logo si non défini
    if not params.get('logo'):
        params['logo'] = 'logo_default.png'
    return dict(parametres=params)

with app.app_context():
    db.create_all()
    if not User.query.first():
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True) 