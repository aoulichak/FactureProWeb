from . import db

class Parametres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cle = db.Column(db.String(50), unique=True, nullable=False)
    valeur = db.Column(db.Text, nullable=False) 