# Hotel California
## Présentation
Ce projet Django est un système fictif de gestion de l'hotel California.
C'est un serveur qui a été mis à disposition des participants du sujet pour interagir avec l'hotel.


## Installation & Usage
### Utilisation par docker
- Créer une copie du fichier `.env.example` en `.env` pour positionner les variables d'environnement nécessaires.
- Exécuter la commande suivante pour lancer le serveur : `docker-compose up -d --build`  
- Pour voir les logs : `docker-compose logs -f`
- Pour arrêter : `docker-compose down`


### Par python en local avec Django
- Créer une copie du fichier `.env.example` en `.env` pour positionner les variables d'environnement nécessaires.
- Exécuter `python manage.py runserver`


### Deployment sur GCP (google)
- Créer une copie du fichier `.env.example` en `.env.yaml` pour les variables d'environnement
- Exécuter `gcloud run deploy app --port 8000 --source . --env-vars-file .env.yaml --region europe-west9 --project school-of-ai-447610`  


## Initialisation de la base de données
Lors de la première utilisation la base de données sera créée mais contiendra uniquement l'administrateur.

Il faut se connecter avec l'administrateur sur la page `localhost:8000/user_home` et cliquer sur "Reset all datas in app" pour créer les utilisateurs des équipes et initialiser les données des équipes.

Les logins, mots de passe et clefs d'API créées par défaut pour les utilisateurs des équipes sont consultables dans le fichier `hotel_california_app/datas/users.json`


## Authentification pour les API
Exemple d'usage en curl : `curl -H "Authorization: Token <APIKEY>" http://<HOST>/api/`


## Usage
- `localhost:8000` pour accéder à l'interface web
- `localhost:8000/admin` pour accéder à l'interface d'administration Django
- `localhost:8000/user_home` pour accéder à l'interface mise à disposition des participants
- `localhost:8000/api` pour accéder à l'API, authentification via API key
- `localhost:8000/reset` pour réinitialiser la base de données, à lancer une première fois pour initialiser les données, il faut être authentifié via `/admin`
