# 24hcode2025


## Prérequis
Python 3.12 ou supérieur
Requirements dans `hotel_california/requirements.txt` ou `24hcode_public/requirements.txt`  
Docker et dockercompose pour deployer facilement

## Hotel California
Système de gestion de l'hotel California pour les participants du sujet.

### Usage
- `localhost:8000` pour accéder à l'interface web
- `localhost:8000/admin` pour accéder à l'interface d'administration
- `localhost:8000/api` pour accéder à l'API, authentification via API key
- `localhost:8000/reset` pour réinitialiser la base de données, à lancer une première fois pour initialiser les données, il faut être authentifié via `/admin`


## 24hcode Public
Application prototype du sujet de la school of AI pour les 24h du code 2025, mais également utilisable dans le futur. Au lieu de se connecter au SI de l'hotel California, elle se connecte à des données liées à l'événement (dans l'app directement).

