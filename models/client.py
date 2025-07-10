from . import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_complet = db.Column(db.String(200), nullable=False)
    entreprise = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telephone = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f'<Client {self.nom_complet}>' 