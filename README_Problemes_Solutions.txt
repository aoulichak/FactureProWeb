FacturePro - Problèmes Courants et Solutions
===========================================

1. Problème : Impossible de se connecter (mot de passe oublié ou admin supprimé)
-------------------------------------------------------------------------------
Solution :
- Utiliser la fonction de réinitialisation totale dans les paramètres (si accessible).
- Sinon, supprimer la base de données `facturepro.db` et relancer l'application pour recréer l'admin par défaut (admin/admin123).

2. Problème : Erreur lors de la génération du PDF (WeasyPrint, xhtml2pdf)
------------------------------------------------------------------------
Solution :
- Vérifier que xhtml2pdf est bien installé (`pip install xhtml2pdf`).
- S'assurer que le chemin du logo est correct et que le fichier existe.
- Pour Windows, privilégier xhtml2pdf (plus compatible).

3. Problème : Logo non affiché ou upload impossible
--------------------------------------------------
Solution :
- Vérifier les droits d'écriture sur le dossier `static/img/`.
- S'assurer que le fichier uploadé est bien une image (png, jpg, jpeg, gif).
- Le nom du fichier doit être `logo_custom.png` (par défaut).

4. Problème : Messages flash non affichés
-----------------------------------------
Solution :
- Vérifier que le bloc d'affichage des messages flash est bien présent dans le template concerné (voir exemple dans `parametres.html`).

5. Problème : Problème d'encodage (caractères spéciaux, PDF, Excel)
-------------------------------------------------------------------
Solution :
- S'assurer que tous les fichiers sont enregistrés en UTF-8.
- Pour Excel, utiliser `pandas` et `openpyxl` pour garantir la compatibilité.

6. Problème : Erreur "Could not build url for endpoint 'login'"
--------------------------------------------------------------
Solution :
- Utiliser le bon nom d'endpoint dans `url_for` (ex : `auth.login` au lieu de `login`).
- Vérifier les blueprints et les routes dans `app.py` et `routes/auth.py`.

7. Problème : Problème de migration ou de structure de base
-----------------------------------------------------------
Solution :
- Si un champ a été ajouté à un modèle, supprimer la base et relancer pour la régénérer (en développement).
- En production, utiliser un outil de migration (ex : Flask-Migrate).

8. Problème : Problème d'accès ou de droits (403, 404)
------------------------------------------------------
Solution :
- Vérifier que l'utilisateur est bien connecté et a le bon rôle.
- Vérifier les décorateurs `@login_required` et `@admin_required`.

9. Problème : Problème d'affichage responsive ou CSS
----------------------------------------------------
Solution :
- Forcer le rechargement du CSS (Ctrl+F5).
- Vérifier que le fichier `style.css` est bien chargé dans le template.

10. Problème : Problème d'upload ou de suppression de données
------------------------------------------------------------
Solution :
- Vérifier les droits sur le dossier `instance/` et `static/img/`.
- Vérifier les messages d'erreur dans la console Flask.

Pour tout autre problème, consulter les logs de l'application, vérifier la documentation technique, ou demander de l'aide au développeur. 