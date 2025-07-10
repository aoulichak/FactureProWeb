from . import db

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    prix = db.Column(db.Float, nullable=False)
    type_prix = db.Column(db.String(10), nullable=False)  # 'HT' ou 'TTC'
    tva = db.Column(db.Float, nullable=False)  # en pourcentage

    def __repr__(self):
        return f'<Produit {self.nom}>' 