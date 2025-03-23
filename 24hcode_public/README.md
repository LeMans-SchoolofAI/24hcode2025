# 24hcode_public
## Présentation
Application prototype du sujet de la school of AI pour les 24h du code 2025, mais également utilisable dans le futur. Au lieu de se connecter au SI de l'hotel California, elle se connecte à des données liées à l'événement (dans l'app directement).

### Usage du speech to text
Pour pouvoir utiliser correctement le speech to text, il faut un fichier audio de référence pour utiliser la voix. J'ai mis un script dans 24hcode_public/public_app/micro.py pour enregistrer 120 secondes d'audio avec le micro du PC.
J'ai rajouté une consigne à l'agent pour enlever les abréviations et les nombres écris en chiffres, sinon le modèle audio est nul.
Pour l'auto play sur le navigateur, il faut l'autoriser dans les paramètres du navigateur.

## Installation & Usage
### Utilisation par docker
- Créer une copie du fichier `.env.example` en `.env` pour positionner les variables d'environnement nécessaires.
- Exécuter la commande suivante pour lancer le serveur : `docker-compose up -d --build`  
- Pour voir les logs : `docker-compose logs -f`
- Pour arrêter : `docker-compose down`
