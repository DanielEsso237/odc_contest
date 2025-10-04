Application Django - ODC_CONTEST
Bienvenue dans le projet d'application Django pour la gestion des concours de ODC et autres. Ce document explique comment configurer et exécuter l'application en local pour les tests, en utilisant une base de données SQLite.

Étapes pour exécuter l'application en local
1. Cloner le dépôt
Clonez le dépôt GitHub et passez à la branche test/sqlite-config :
git clone <https://github.com/DanielEsso237/odc_contest.git>
cd <ODC_CONTEST>
git checkout test/sqlite-config

2. Créer un environnement virtuel
Créez et activez un environnement virtuel pour isoler les dépendances :
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

3. Installer les dépendances
Installez les packages requis listés dans requirements.txt :
pip install -r requirements.txt

4. Configurer la base de données
La branche test/sqlite-config utilise SQLite, donc aucune installation de base de données n’est nécessaire. Appliquez les migrations pour créer la base de données :
python manage.py migrate

5. (Obligatoire) Créer un superutilisateur:Le super utilisateur sera l'administrateur technique de l application
Pour accéder à l’interface d’administration Django, créez un superutilisateur :
python manage.py createsuperuser

6. Lancer le serveur
Démarrez le serveur de développement Django :
python manage.py runserver

Ouvrez votre navigateur et accédez à http://localhost:8000 pour voir l’application.
7. Testez l'application :

A - Créons un modo :

a. Creez un compte

b. Connectez vous en tant que admin, allez dans utilisateurs, choisissez le compte et modifiez la role du compte de membre à Modérateur et sauvegardez

c.Connectez vous en tant que modérateur avec les identifiants crées ci dessous

d. Accedez à la partie "gérer les évènements" dans le header, creez un évènement (ex:miss odc)



URLs principales :
/contests/events/ : Liste des événements
/contests/trials/<event_id>/ : Liste des épreuves pour un événement
/contests/publications/<trial_id>/ : Publications d’une épreuve
/contests/ranking/<trial_id>/ : Classement d’une épreuve
/admin/ : Interface d’administration (connectez-vous avec le superutilisateur)


Fonctionnalités à tester :
Navigation entre les événements, épreuves, publications, et classements.
Ajout d’une épreuve (nécessite un rôle de modérateur).
Interaction avec le carrousel de médias dans les publications.
Vote sur les publications (vérifiez si les compteurs de votes se mettent à jour).
Affichage du modal pour ajouter une épreuve.



8. (Facultatif) Données de test
Pour remplir la base de données avec des données de test, exécutez :
python manage.py loaddata <nom_du_fichier_de_données>.json

Note : Vérifiez si des fichiers de données (fixtures) sont inclus dans le projet.
Structure du projet

contests/templates/contests/ : Contient les fichiers HTML (events.html, trials.html, publications.html, ranking.html).
contests/static/contests/css/ : Fichiers CSS pour le style.
contests/static/contests/js/ : Fichiers JavaScript pour l’interactivité.
contests/settings.py : Configuration de l’application, avec SQLite pour cette branche.

Remarques

Cette branche utilise SQLite pour simplifier les tests locaux. La branche principale (main) utilise PostgreSQL.
Si vous rencontrez des erreurs liées aux migrations, vérifiez la compatibilité des modèles avec SQLite (par exemple, certains champs spécifiques à PostgreSQL peuvent poser problème).
Signalez tout bug ou problème dans les issues GitHub ou contactez le mainteneur.

Problèmes courants

Erreur de dépendances : Assurez-vous que toutes les dépendances dans requirements.txt sont installées.
Erreur de migrations : Supprimez le fichier db.sqlite3 et réexécutez python manage.py migrate.
Carrousel cassé : Vérifiez la console du navigateur (F12) pour des erreurs JavaScript ou CSS.

Contribuer
Pour proposer des modifications :

Créez une branche à partir de test/sqlite-config (par exemple, fix/<nom_du_correctif>).
Faites vos modifications et testez localement.
Poussez votre branche et créez une pull request vers test/sqlite-config.

Merci de tester l’application ! Pour toute question, contactez .