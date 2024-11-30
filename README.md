# 24hcode2025
## Prérequis
* Python 3.12 ou supérieur (si dev local, sinon juste déploiement, pas besoin)  
* ffmpeg pour whisper pour 24hcode_public (si dev local, sinon juste déploiement, pas besoin)  
* Requirements dans `hotel_california/requirements.txt` ou `24hcode_public/requirements.txt`  
* Docker et dockercompose pour deployer facilement

## Installation & Usage
Par docker :
- Allez dans le répertoire souhaité (hotel_california ou 24hcode_public) et exécutez les commandes suivantes :
`docker-compose up -d --build`  
- Pour voir les logs : `docker-compose logs -f`  
- Pour arrêter : `docker-compose down`

Par python en local avec Django :
- Allez dans le répertoire souhaité (hotel_california ou 24hcode_public) et exécuter `python manage.py runserver`

Attention : pour le premier lancement il faut obligatoirement commencer par docker car les variables d'environnement pour la création du superuser par défaut sont dans le docker-compose.yml (sinon il faut les mettre en variable d'environnement du terminal avant de lancer `python manage.py runserver`)

## Hotel California
Système de gestion de l'hotel California pour les participants du sujet.

### Authentification
Exemple d'usage en curl : `curl -H "Authorization: Token <APIKEY>" http://<HOST>/api/`

### Usage
- `localhost:8000` pour accéder à l'interface web
- `localhost:8000/admin` pour accéder à l'interface d'administration
- `localhost:8000/api` pour accéder à l'API, authentification via API key
- `localhost:8000/reset` pour réinitialiser la base de données, à lancer une première fois pour initialiser les données, il faut être authentifié via `/admin`


## 24hcode Public
Application prototype du sujet de la school of AI pour les 24h du code 2025, mais également utilisable dans le futur. Au lieu de se connecter au SI de l'hotel California, elle se connecte à des données liées à l'événement (dans l'app directement).

## Concierge
Prototype de concierge virtuel pouvant accéder aux API de l'hôtel California

### Installation
Créer un fichier `.env` dans le répertoire `concierge` et y ajouter les variables d'environnement suivantes :
- `LLM_API_URL` : URL de l'API du fournisseur de LLM
- `LLM_API_KEY` : clef d'API de l'utilisateur pour le LLM (vide si utilisation ollama ou LMStudio)
- `API_USERNAME` : nom d'utilisateur de l'API de l'hôtel California
- `API_TOKEN` : clef d'API de l'utilisateur de l'API de l'hôtel California
- `LANG_FUSE_SECRET_KEY` : secret key de Langfuse (optionnel si utilisation de Langfuse)
- `LANG_FUSE_PUBLIC_KEY` : public kety de l'instance de Langfuse utilisée (optionnel si utilisation de Langfuse)
- `LANG_FUSE_HOST` : URL de l'instance de Langfuse utilisée (optionnel si utilisation de Langfuse)
- `MISTRAL_API_KEY` : clef d'API pour Mistral
- `HOTEL_API_URL`: URL de l'API de l'hôtel California, par exemple `HOTEL_API_URL='http://localhost:8000/api'
- `HOTEL_API_TOKEN`: token de l'utilisateur de l'API de l'hôtel California

### Usage
- `python concierge.py` pour lancer l'application

## FAQ

### Langfuse

[Langfuse](https://langfuse.com) est un concurrent opensource de langsmith qui est utilisé pour surveiller le comportement de l'agent, son utilisation est optionnelle. Il est possible de l'utiliser en mode cloud (potentiellement payant) ou de le lancer en local avec docker.

A noter : en développement l'execution avec Docker est le plus simple mais l'instance ne garde pas les données entre chaque démarrage : https://langfuse.com/docs/deployment/local



