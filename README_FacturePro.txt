FacturePro - Application Web de Facturation Professionnelle
===========================================================

Présentation Générale
---------------------
FacturePro est une application web moderne de gestion de factures, clients et produits, conçue pour les professionnels et TPE/PME. Elle permet de gérer l'ensemble du cycle de facturation, d'administrer les paramètres de l'entreprise, de générer des PDF professionnels, et d'obtenir des statistiques et rapports avancés.

Technologies utilisées
---------------------
- Python 3, Flask (backend web)
- SQLite (base de données légère)
- Bootstrap 5 (UI responsive et moderne)
- JavaScript (interactions dynamiques, animations)
- xhtml2pdf (génération de PDF compatible Windows)

Fonctionnalités principales
--------------------------
1. Authentification admin sécurisée (compte par défaut : admin/admin123, modifiable)
2. Gestion des clients (CRUD complet, recherche, navigation fluide)
3. Gestion des produits (CRUD, description, type de prix, TVA, aperçu, sélection intelligente)
4. Gestion des factures :
   - Création dynamique (sélection client, produits, quantités, prix, TVA, type prix)
   - Calculs automatiques HT/TVA/TTC
   - Visualisation détaillée
   - Modification et suppression
   - Génération de PDF professionnel (en-tête, logo, conditions, signature, Dirham marocain)
   - Ajout du champ "Commande n°", suppression du champ "Échéance"
5. Dashboard interactif :
   - Indicateurs clés (nombre de clients, factures, montants, TVA)
   - Graphiques dynamiques (CA, top clients, histogramme factures)
   - Tableau des 5 dernières factures
   - Encadré de performance mensuelle
   - Animations et design moderne
6. Page Paramètres :
   - Modification des infos société (nom, adresse, email, téléphone, logo)
   - Modification des conditions de paiement
   - Modification du login/mot de passe admin
   - Suppression totale de toutes les données (avec saisie du mot de passe, recréation admin par défaut)
7. Génération et téléchargement de rapports Excel filtrés (mois, année, jour, client, produit)
8. Recherche professionnelle dans les factures (par client, date, suggestions dynamiques)
9. Affichage dynamique du logo dans la navbar, le PDF, la page de connexion
10. Sécurité : accès restreint, gestion des sessions, vérification du mot de passe pour les actions sensibles

Structure du projet
------------------
- FactureProWeb/
  - app.py : point d'entrée Flask, configuration, blueprints
  - models/ : modèles SQLAlchemy (User, Client, Produit, Facture, LigneFacture, Parametres)
  - routes/ : blueprints Flask (auth, clients, produits, factures, dashboard, parametres)
  - templates/ : templates HTML Jinja2 (Bootstrap, responsive, animations)
  - static/ : fichiers statiques (CSS, images, logo)
  - requirements.txt : dépendances Python
- instance/
  - facturepro.db : base de données SQLite

Logique métier et UX/UI
-----------------------
- Navigation fluide et intuitive, design épuré et professionnel
- Formulaires adaptés, validation, messages flash clairs
- Sélection intelligente des produits lors de la création de facture (pas de doublons)
- Calculs automatiques et affichage clair des totaux
- PDF généré avec toutes les informations dynamiques de l'entreprise
- Dashboard animé, indicateurs et graphiques interactifs
- Page paramètres complète, gestion du logo, sécurité renforcée
- Option de réinitialisation totale de la base (avec confirmation et mot de passe)

Points techniques et robustesse
-------------------------------
- Calculs de TVA et totaux conformes aux standards
- Gestion des fichiers upload (logo) sécurisée
- Protection contre les imports circulaires
- Gestion des erreurs et messages utilisateur améliorée
- Compatibilité Windows (xhtml2pdf)
- Injection dynamique des paramètres d'entreprise dans tous les templates
- Sécurité des routes (login_required, vérification du mot de passe)

Personnalisation et évolutivité
------------------------------
- Facilement personnalisable (logo, couleurs, conditions, etc.)
- Code structuré, prêt pour extensions (multi-utilisateurs, multi-sociétés, etc.)

Auteur :
--------
Développé par Mohamed (et assisté par IA)

Pour toute question ou évolution, voir le code source ou contacter le développeur. 