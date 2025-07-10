FacturePro - FAQ (Foire Aux Questions)
======================================

Q1 : Comment réinitialiser le mot de passe administrateur ?
-----------------------------------------------------------
R : Utilisez la fonction de réinitialisation totale dans les paramètres (saisie du mot de passe). Sinon, supprimez la base `facturepro.db` pour recréer l'admin par défaut (admin/admin123).

Q2 : Comment ajouter un logo personnalisé à mes factures ?
---------------------------------------------------------
R : Allez dans Paramètres > Logo, uploadez votre image (png, jpg, jpeg, gif). Le logo apparaîtra sur toutes les factures et dans la barre de navigation.

Q3 : Comment générer un rapport Excel filtré ?
----------------------------------------------
R : Sur la page Factures, utilisez la section "Rapports Excel" pour choisir vos filtres (mois, année, client, produit) puis cliquez sur "Télécharger".

Q4 : Puis-je ajouter plusieurs utilisateurs (employés) ?
--------------------------------------------------------
R : Oui, voir le fichier `README_MultiUser_FacturePro.txt` pour l'extension multi-utilisateurs avec rôles et accès limités.

Q5 : Comment déployer FacturePro sur un serveur cloud ?
-------------------------------------------------------
R : Suivez les instructions du fichier `README_Deployment_MultiSociete.txt` pour un déploiement multi-entreprises (SaaS) sur Heroku, Render, AWS, etc.

Q6 : Est-ce que mes données sont sécurisées ?
---------------------------------------------
R : Oui, voir le fichier `README_Securite_FacturePro.txt` pour toutes les bonnes pratiques appliquées (authentification, hashage, filtrage, HTTPS, etc.).

Q7 : Comment connecter FacturePro à une base cloud (Firebase) ?
--------------------------------------------------------------
R : Suivez le guide dans `README_Firebase_FacturePro.txt` pour migrer ou synchroniser vos données avec Firestore.

Q8 : Que faire en cas d'erreur ou de bug ?
-----------------------------------------
R : Consultez le fichier `README_Problemes_Solutions.txt` pour les solutions aux problèmes courants. Sinon, vérifiez les logs ou contactez le développeur.

Q9 : Peut-on personnaliser l'apparence (couleurs, logo, en-tête) ?
------------------------------------------------------------------
R : Oui, via la page Paramètres pour le logo et les infos société. Pour les couleurs, modifiez le fichier `static/css/style.css`.

Q10 : Comment ajouter une nouvelle fonctionnalité ?
--------------------------------------------------
R : Consultez la documentation technique (`README_Technique_FacturePro.txt`) et suivez la structure des blueprints et modèles. Le code est modulaire et prêt pour l'extension. 