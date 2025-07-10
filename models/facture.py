from . import db

class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    commande_num = db.Column(db.String(50), nullable=True)
    lignes = db.relationship('LigneFacture', backref='facture', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Facture {self.id}>'

class LigneFacture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facture_id = db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    type_prix = db.Column(db.String(10), nullable=False)  # 'HT' ou 'TTC'
    tva = db.Column(db.Float, nullable=False)
    nom_produit = db.Column(db.String(150), nullable=False)  # snapshot du nom au moment de la facture

    def __repr__(self):
        return f'<LigneFacture {self.id}>' 