# Dockerfile

# Utiliser une image de base officielle de Python
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

RUN touch /etc/apt/apt.conf
RUN echo 'Acquire::http::proxy "http://proxyweb.sorbonne-universite.fr:3128";' >> /etc/apt/apt.conf
RUN echo 'Acquire::https::proxy "http://proxyweb.sorbonne-universite.fr:3128";' >> /etc/apt/apt.conf
RUN echo 'Acquire::ftp::proxy "http://proxyweb.sorbonne-universite.fr:3128";'  >> /etc/apt/apt.conf
ENV http_proxy="http://proxyweb.sorbonne-universite.fr:3128"
ENV https_proxy="http://proxyweb.sorbonne-universite.fr:3128"

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier tout le contenu du projet dans le conteneur
COPY . .

# Exposer le port sur lequel Django va tourner (8000 par défaut)
EXPOSE 8000

# Lancer le script de démarrage
CMD ["./start.sh"]
