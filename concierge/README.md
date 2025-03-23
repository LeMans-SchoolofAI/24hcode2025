# Concierge
## Présentation
Ce soddier contient différents prototypes de concierge virtuel pouvant accéder aux API de l'hôtel California

## Installation
Copier le fichier `.env.example` en fichier `.env` et remplacer les variables d'environnement :
- `LLM_PROVIDER`: provider de LLM (`Mistral` ou `Google`)
- `MISTRAL_API_KEY` ou `GOOGLE_API_KEY`: clef d'API pour Mistral ou Google
- `LANG_FUSE_SECRET_KEY` : secret key de Langfuse (optionnel si utilisation de Langfuse)
- `LANG_FUSE_PUBLIC_KEY` : public kety de l'instance de Langfuse utilisée (optionnel si utilisation de Langfuse)
- `LANG_FUSE_HOST` : URL de l'instance de Langfuse utilisée (optionnel si utilisation de Langfuse)
- `HOTEL_API_URL`: URL de l'API de l'hôtel California, par exemple `HOTEL_API_URL='http://localhost:8000/api'
- `HOTEL_API_TOKEN`: token de l'utilisateur de l'API de l'hôtel California

## Usage
- Lancer préalablement LangFuse pour surveiller le comportement de l'agent (optionnel), sinon il est préférable de changer la variable `DEBUG_LANGFUSE` pour la valeur `False` dans le fichier Python
- Lancer l'un des fichiers python concierge en fonction de la version souhaitée
   - `python concierge.py` pour lancer l'application en mode texte simple dans le teminal
   - `python -m streamlit run concierge_st.py` pour lancer l'application avec Streamlit
   - `python -m streamlit run concierge_st_kokoro.py` pour lancer l'application avec Streamlit avec kokoro


### Langfuse

[Langfuse](https://langfuse.com) est un concurrent opensource de langsmith qui est utilisé pour surveiller le comportement de l'agent, son utilisation est optionnelle. Il est possible de l'utiliser en mode cloud (potentiellement payant) ou de le lancer en local avec docker.
