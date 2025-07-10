FacturePro - Sécurité : Bonnes Pratiques et Recommandations
==========================================================

1. Authentification et gestion des utilisateurs
----------------------------------------------
- Utiliser Flask-Login pour la gestion des sessions et l'authentification.
- Hasher tous les mots de passe avec Werkzeug (jamais de stockage en clair).
- Forcer des mots de passe forts lors de la création/modification de compte.
- Limiter le nombre de tentatives de connexion (anti-bruteforce, ex : Flask-Limiter).
- Déconnexion automatique après inactivité (timeout de session).

2. Gestion des accès et des rôles
---------------------------------
- Protéger toutes les routes sensibles avec @login_required.
- Utiliser des décorateurs personnalisés pour les accès admin (ex : @admin_required).
- Masquer les actions réservées à l'admin dans les templates.
- Toujours vérifier le rôle côté backend (jamais seulement côté frontend).

3. Sécurité des données
----------------------
- Filtrer toutes les requêtes par l'identifiant de société (multi-tenancy).
- Ne jamais exposer d'identifiants sensibles dans les URLs ou le frontend.
- Protéger les fichiers uploadés (logo) :
  - Vérifier l'extension et le type MIME
  - Limiter la taille
  - Stocker dans un dossier sécurisé (ex : static/img/)
- Sauvegarder régulièrement la base de données.

4. Sécurité des formulaires et du code
--------------------------------------
- Valider et nettoyer toutes les entrées utilisateur (anti-injection SQL, XSS).
- Utiliser les filtres Jinja2 pour échapper les variables dans les templates.
- Protéger les formulaires sensibles par la saisie du mot de passe (ex : suppression totale).
- Utiliser des tokens CSRF (ex : Flask-WTF) pour tous les formulaires POST.

5. Sécurité du déploiement
--------------------------
- Toujours utiliser HTTPS en production (certificat SSL).
- Protéger les variables d'environnement (clé secrète, DB URI, credentials Firebase…)
- Garder le serveur et les dépendances à jour (pip freeze > requirements.txt).
- Désactiver le mode debug en production.
- Limiter l'accès SSH/FTP au serveur (firewall, clés SSH).

6. Extensions et surveillance
----------------------------
- Journaliser les actions critiques (connexion, suppression, export…)
- Ajouter une page d'audit pour l'admin (historique des actions)
- Mettre en place une alerte email en cas d'action sensible (optionnel)

7. Exemples de code
-------------------
- Hashage du mot de passe :
  ```python
  from werkzeug.security import generate_password_hash
  user.password_hash = generate_password_hash(password)
  ```
- Vérification du rôle :
  ```python
  if not current_user.is_authenticated or current_user.role != 'admin':
      abort(403)
  ```
- Validation d'un fichier uploadé :
  ```python
  ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
  def allowed_file(filename):
      return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  ```

Pour aller plus loin :
----------------------
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Guide](https://flask.palletsprojects.com/en/latest/security/)

En appliquant ces recommandations, FacturePro sera robuste, sécurisé et conforme aux bonnes pratiques professionnelles. 