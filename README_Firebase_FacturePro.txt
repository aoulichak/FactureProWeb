FacturePro - Connexion à une base de données Cloud (Firebase/Firestore)
======================================================================

Objectif
--------
Remplacer ou compléter la base SQLite locale par une base de données cloud (ex : Firebase Firestore) pour permettre l'accès multi-appareils, la sauvegarde distante, et la synchronisation en temps réel.

1. Choix de la solution cloud
-----------------------------
- Firebase Firestore (NoSQL, temps réel, facile à intégrer avec Python via REST ou bibliothèques tierces)
- Alternatives : MongoDB Atlas, Google Cloud SQL, Amazon RDS, etc.

2. Pré-requis Firebase
----------------------
- Créer un projet sur https://console.firebase.google.com/
- Activer Firestore Database
- Récupérer les identifiants du projet (clé API, etc.)
- Installer la bibliothèque Python :
  ```bash
  pip install google-cloud-firestore
  ```

3. Exemple de connexion et opérations de base
---------------------------------------------
Dans un nouveau fichier `firebase_utils.py` :

```python
import os
from google.cloud import firestore

# Initialisation (utiliser le fichier de credentials JSON téléchargé depuis Firebase)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "chemin/vers/credentials.json"
db = firestore.Client()

# Exemple : ajouter un client
client_data = {
    'nom_complet': 'Ali Benali',
    'entreprise': 'ABC SARL',
    'email': 'ali@abc.com',
    'telephone': '0600000000'
}
db.collection('clients').add(client_data)

# Exemple : récupérer tous les clients
clients = db.collection('clients').stream()
for doc in clients:
    print(doc.id, doc.to_dict())
```

4. Adapter les modèles et routes
-------------------------------
- Remplacer les requêtes SQLAlchemy par des appels Firestore (CRUD)
- Exemple pour récupérer tous les clients :
  ```python
  def get_all_clients():
      return [doc.to_dict() for doc in db.collection('clients').stream()]
  ```
- Adapter la logique de création, modification, suppression, etc.

5. Points d'attention
---------------------
- Firestore est NoSQL : la structure des données est différente (collections, documents)
- Les relations (ex : factures liées à un client) doivent être gérées manuellement (stockage d'ID, requêtes croisées)
- Les opérations sont asynchrones (penser à la gestion des retours)
- Sécurité : bien configurer les règles d'accès Firestore
- Coût : Firestore est gratuit jusqu'à un certain quota, puis payant

6. Extensions possibles
----------------------
- Utiliser Firebase Auth pour la gestion des utilisateurs
- Synchronisation temps réel (écoute des changements)
- Sauvegarde automatique et restauration

7. Ressources utiles
--------------------
- [Documentation officielle Firestore Python](https://googleapis.dev/python/firestore/latest/index.html)
- [Exemple Flask + Firestore](https://github.com/googleapis/python-firestore/tree/main/samples/snippets)

Cette intégration permet de rendre FacturePro accessible partout, de sécuriser les données et d'ouvrir la voie à des fonctionnalités avancées (multi-utilisateurs, mobile, etc.). 