FacturePro - Documentation Technique
===================================

1. Architecture Générale
------------------------
- Application Flask structurée en blueprints (auth, clients, produits, factures, dashboard, parametres).
- Base de données SQLite (SQLAlchemy ORM).
- Frontend basé sur Bootstrap 5, templates Jinja2, et JavaScript pour l'interactivité.
- Génération de PDF avec xhtml2pdf (compatibilité Windows).

2. Structure des fichiers
-------------------------
- FactureProWeb/
  - app.py : configuration Flask, enregistrement des blueprints, injection des paramètres globaux.
  - models/
    - user.py : modèle User (authentification, hash du mot de passe)
    - client.py : modèle Client
    - produit.py : modèle Produit
    - facture.py : modèles Facture et LigneFacture (relation, cascade delete)
    - parametres.py : modèle Parametres (clé/valeur pour infos société)
  - routes/
    - auth.py : login/logout
    - clients.py : CRUD clients
    - produits.py : CRUD produits
    - factures.py : gestion factures, PDF, recherche
    - dashboard.py : statistiques, graphiques
    - parametres.py : gestion des paramètres, réinitialisation totale
  - templates/ : HTML Jinja2 (Bootstrap, responsive, animations)
  - static/ : CSS, images, logo
  - requirements.txt : dépendances Python
- instance/
  - facturepro.db : base SQLite

3. Modèles de données (SQLAlchemy)
----------------------------------
- User : id, username, password_hash (hashé avec Werkzeug)
- Client : id, nom_complet, entreprise, email, téléphone
- Produit : id, nom, description, prix, type_prix, tva
- Facture : id, client_id (FK), date, commande_num, lignes (relation)
- LigneFacture : id, facture_id (FK), produit_id (FK), quantite, prix, type_prix, tva, nom_produit
- Parametres : id, cle, valeur

4. Sécurité
-----------
- Authentification obligatoire (Flask-Login, login_required sur toutes les routes sensibles)
- Hashage des mots de passe (Werkzeug)
- Modification du mot de passe admin possible dans les paramètres
- Suppression totale des données protégée par saisie du mot de passe
- Gestion des sessions sécurisée
- Upload de logo contrôlé (chemin sécurisé, extension image)

5. Logique métier
-----------------
- Calculs automatiques HT/TVA/TTC lors de la création/édition de facture
- Sélection dynamique des produits (pas de doublons dans une facture)
- Génération de PDF avec toutes les infos dynamiques (logo, société, conditions)
- Dashboard : agrégation SQL pour les indicateurs et graphiques
- Génération de rapports Excel filtrés (BytesIO, pandas)
- Injection dynamique des paramètres d'entreprise dans tous les templates via context_processor

6. Robustesse et bonnes pratiques
---------------------------------
- Protection contre les imports circulaires (import locaux dans les routes critiques)
- Gestion des erreurs utilisateur (messages flash, validations de formulaire)
- Suppression en cascade (LigneFacture supprimées avec Facture)
- Nettoyage du logo lors de l'upload (remplacement du fichier)
- Compatibilité Windows (xhtml2pdf, chemins d'accès)
- Code modulaire, facilement extensible

7. Dépendances principales
-------------------------
- Flask, Flask-Login, Flask-SQLAlchemy
- Werkzeug (hashage)
- Bootstrap 5 (CDN)
- xhtml2pdf (PDF)
- pandas, openpyxl (rapports Excel)

8. Points d'extension possibles
------------------------------
- Multi-utilisateurs, multi-sociétés
- Gestion des droits/permissions
- Export/import de la base
- API REST pour intégration externe

Pour toute évolution technique, se référer au code source et à la structure ci-dessus. 