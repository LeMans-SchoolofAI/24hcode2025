#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

# Créer les migrations
echo "make database migrations..."
python manage.py makemigrations --noinput

# Appliquer les migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Créer le superutilisateur si aucun n'existe
echo "Creating superuser if it doesn't exist..."
python manage.py createsuperuser --noinput

# Démarrer le serveur Django
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000