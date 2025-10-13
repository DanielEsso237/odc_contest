ODC CONTEEST— Plateforme communautaire de concours et votes

Bienvenue sur ODC CONTEST, une application web développée avec Django qui permet à une communauté d’otakus de créer, gérer et participer à des concours, épreuves et votes !
Ce projet met en avant l’organisation d’évènements, la soumission de participations, et la modération communautaire.

I/ Fonctionnalités principales

- Authentification utilisateur (Admin, Modérateur, Membre/Participant)

- Espace d’administration Django pour la gestion complète du site

- Création et gestion d’évènements (concours, tournois, etc.)

- Création d’épreuves associées à un évènement

- Ajout et gestion des participants

- Soumission de participations aux épreuves

- Validation et gestion des soumissions par les modérateurs

- Fil d’actualité affichant les activités récentes (concours, soumissions validées, etc.)

II/ Installation et configuration
1. Cloner le dépôt
git clone https://github.com/DanielEsso237/odc_contest.git
cd otaku-vote
git checkout test/sqlite-config

2. Créer et activer un environnement virtuel
python -m venv venv
venv\Scripts\activate  # sous Windows
source venv/bin/activate  # sous macOS / Linux

3. Installer les dépendances
pip install -r requirements.txt

4. Effectuer les migrations et lancer le serveur
python manage.py migrate
python manage.py runserver

III/ Guide de test rapide

Voici les étapes pour tester les fonctionnalités de modo de l'application :

Étape 1 — Créer un compte administrateur

Crée un superutilisateur pour accéder à l’administration Django :

python manage.py createsuperuser

Étape 2 — Créer un compte standard

- Ouvre l’application dans ton navigateur : http://127.0.0.1:8000

- Inscris-toi via le formulaire de registre (par exemple : modo1).

Étape 3 — Promouvoir le compte en modérateur

- Connecte-toi à l’interface d’administration Django : http://127.0.0.1:8000/admin

- Modifie le compte modo1 et change son statut de membre en modérateur.

Étape 4 — Créer d’autres comptes standard

- Crée quelques utilisateurs via le formulaire d’inscription (pour tester la gestion des participants).

Étape 5 — Se connecter en modérateur

- Connecte-toi avec modo1.

- Va dans Gérer les évènements → Créer un évènement.

Étape 6 — Créer une épreuve

- Accède à Gérer → Épreuves → Créer une épreuve.

- L’épreuve sera associée à ton évènement.

Étape 7 — Ajouter des participants

- Va dans Gérer un évènement, choisi un concours choisis gerer, puis  Participants.

- Sélectionne un concours et ajoute des membres comme participants.
(Ces comptes seront désormais inscrits à l’épreuve.)

Étape 8 — Se connecter en tant que participant

- Connecte-toi avec un compte membre ajouté à l’épreuve(un compte participant)

- Va sur Soumettre et remplis le formulaire pour envoyer ta participation.

Étape 9 — Validation de la soumission

- Reconnecte-toi avec le compte modérateur (modo1).

- Va dans Gérer les évènements → Gérer → Épreuve → Gérer les soumissions.

- Ouvre une soumission, examine-la en détail et valide-la.

Étape 10 — Consulter le fil d’actualité

- Consulte le fil d’actualité pour voir les publiations et voter
