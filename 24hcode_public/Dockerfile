# Dockerfile

# Utiliser une image de base officielle de Python
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# ffmpeg est nécessaire pour whisper
RUN apt update -y && apt install ffmpeg -y

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt
# COPY requirements2.txt .
# RUN pip install -r requirements2.txt

# Copier tout le contenu du projet dans le conteneur
COPY . .

# Exposer le port sur lequel Django va tourner (8000 par défaut)
EXPOSE 8000

# Lancer le script de démarrage
CMD ["./start.sh"]



