import os
import requests

# Load the langchain tools
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Get the environment variables
from dotenv import load_dotenv
load_dotenv()

# Parameters for the hotel APIs
HOTEL_API_URL = os.getenv("HOTEL_API_URL")
HOTEL_API_TOKEN = os.getenv("HOTEL_API_TOKEN")

# Définition des couleurs
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

# Initialize Langfuse handler
DEBUG_LANGUSE = True
if DEBUG_LANGUSE:
    from langfuse.callback import CallbackHandler
    langfuse_handler = CallbackHandler(
        secret_key=os.getenv("LANG_FUSE_SECRET_KEY"),
        public_key=os.getenv("LANG_FUSE_PUBLIC_KEY"),
        host=os.getenv("LANG_FUSE_HOST")
    )
    langfuse_handler.auth_check()
    config = {"callbacks": [langfuse_handler]}
else:
    config = {}

# Define the tools
search_tool = DuckDuckGoSearchRun()

def get_headers():
    return {"Authorization": f"Token {HOTEL_API_TOKEN}"}

@tool
def list_restaurants(page: int = 1) -> [str]:
    """
    Retourne la liste des restaurants de l'hôtel
    
    Args:
        page (int): numéro de page de la recherche
    
    Returns:
        id (str): id technique du restaurant
        name (str): nom du restaurant
        description (str): description du restaurant
        capacity (int): capacité du restaurant
        opening_hours (str): horaires d'ouverture
        location (str): localisation du restaurant dans l'hôtel
        is_active (bool): indique si le restaurant est actif
    Note : la liste retour est paginée
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/restaurants/?page={page}"
    response = requests.get(url, headers=get_headers())
    try:
        data = response.json()
    except:
        data = response
    # Return the list of hotels
    return (data)

@tool
def search_clients(search_term: str, page: int = 1) -> [str]:
    """
    Effectue une recherche sur les clients de l'hôtel

    Args:
        search_term (str): terme de recherche
        page (int): numéro de page de la recherche

    Returns: liste des clients de l'hotel correspondant au terme de recherche.
        id (str): id technique du client
        name (str): nom et prénom du client
        phone_number (str): numéro de téléphone
        room_number (str): numéro de chambre
        special_requests (str): demandes spéciales
    Note : la liste retour est paginée
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/clients/search/?search={search_term}&page={page}"
    response = requests.get(url, headers=get_headers())
    try:
        data = response.json()
    except:
        data = response
    # Return the list of clients
    return (data)

@tool
def list_meals(page: int = 1) -> [str]:
    """
    Retourne la liste des types de repas proposés dans l'hôtel
    
    Args:
        page (int): numéro de page de la recherche
    
    Returns:
        id (int): id technique
        name (str): nom du type de repas
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/meals/?page={page}"
    response = requests.get(url, headers=get_headers())
    try:
        data = response.json()
    except:
        data = response
    # Return the list of meals
    return (data)

@tool
def list_reservations(date_from: str = None, date_to: str = None, id_meal: str = None,
                      id_restaurant: str = None, page: int = 1) -> [str]:
    """
    Retourne la liste des reservations qui répondent aux critères
    
    Args:
        date_from (str): date de debut de la reservation (au format YYYY-MM-DD)
        date_to (str): date de fin de la reservation (au format YYYY-MM-DD)
        id_meal (str): l'id du type de repas (disponible dans la liste des repas)
        id_restaurant (str): l'id du restaurant (disponible dans la liste des restaurants)
        page (int): numéro de page de la recherche
    
    Returns:
        id (str): id technique de la reservation
        client (str): l'id du client
        restaurant (str): l'id du restaurant
        date (str): date de la reservation (au format YYYY-MM-DD)
        meal (str): l'id du type de repas
        number_of_guests (int): le nombre de convives
        special_requests (str): les demandes spéciales
    
    Note:
        Les paramètres sont optionnels, ne transmettre que ceux qui seront utilisés
        La liste retour est paginée
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/reservations/"
    params = {
        "date_from": date_from,
        "date_to": date_to,
        "meal": id_meal,
        "restaurant": id_restaurant,
        "page": page
    }
    filtered_params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, headers=get_headers(), params=filtered_params)
    try:
        data = response.json()
    except:
        data = response
    # Return the list of hotels
    return (data)

@tool
def make_reservation(client: str, restaurant: str, date: str, meal: str, number_of_guests: int, special_requests: str) -> [str]:
    """
    Prend une réservation dans l'un des restaurants de l'hôtel.
    
    Args:
        id_client (str): l'id du client
        id_restaurant (str): l'id du restaurant
        date (str): date de la reservation (au format YYYY-MM-DD)
        id_meal (str): l'id du type de repas (disponible dans la liste des repas)
        number_of_guests (int): le nombre de convives
        special_requests (str): les demandes spéciales

    Note:
        La fonction retourne le resultat de la reservation, qui peut mentionner des erreurs
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/reservations/"
    response = requests.post(url, headers=get_headers(), json={"client": client, "restaurant": restaurant,
                             "date": date, "meal": meal, "number_of_guests": number_of_guests, "special_requests": special_requests})
    try:
        data = response.json()
    except:
        data = response
    # Return the result of the API call
    return (data)

@tool
def modify_reservation(id_reservation: str, id_client: str = None, id_restaurant: str = None, date: str = None,
                       id_meal: str = None, number_of_guests: int = None, special_requests: str = None) -> [str]:
    """
    Modifie une reservation existante

    Args:
        id_reservation (str): id technique de la reservation
        id_client (str): l'id du client
        id_restaurant (str): l'id du restaurant
        date (str): date de la reservation (au format YYYY-MM-DD)
        id_meal (str): l'id du type de repas (disponible dans la liste des repas)
        number_of_guests (int): le nombre de convives
        special_requests (str): les demandes spéciales
    
    Note:
        A l'exception de l'id de la reservation, tous les paramètres sont optionnels, ne transmettre que ceux qui seront modifiés
        La fonction retourne le resultat de la modification, qui peut mentionner des erreurs
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/reservations/{id_reservation}/"
    # Création de la liste des paramètres modifiés
    params = {
        "client": id_client,
        "restaurant": id_restaurant,
        "date": date,
        "meal": id_meal,
        "number_of_guests": number_of_guests,
        "special_requests": special_requests
    }
    # Filtrage des paramètres vides
    filtered_params = {k: v for k, v in params.items() if v is not None}
    response = requests.patch(url, headers=get_headers(), json=filtered_params)
    try:
        data = response.json()
    except:
        data = response
    # Return the result of the API call
    return (data)

def delete_reservation(id_reservation: str) -> [str]:
    """
    Supprime une reservation existante

    Args:
        id_reservation (str): id technique de la reservation

    Note:
        La fonction retourne le resultat de la suppression, qui peut mentionner des erreurs
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/reservations/{id_reservation}/"
    response = requests.delete(url, headers=get_headers())
    try:
        data = response.json()
    except:
        data = response
    # Return the result of the API call
    return (data)

tools = [search_tool, list_restaurants, search_clients, list_meals, list_reservations, make_reservation,
         modify_reservation, delete_reservation]

# Create the agent
memory = MemorySaver()
llm = ChatMistralAI(model="mistral-large-latest", temperature=0, max_retries=2)
agent = create_react_agent(llm, tools, checkpointer=memory)

# Use the agent
# Define a thread_id to track the conversation
config.update({"configurable": {"thread_id": "abc123"}})

# Define the system message and give the agent some context
system_message = SystemMessage(content=
    """Tu es un concierge virtuel pour l'hôtel California. L'hôtel est situé dans la ville du Mans, en France.
       Tu as des outils à ta disposition pour consulter les données de l'hôtel et agir avec le système de l'hôtel.
       Quand un client demande une information, tu lui donne la meilleure information disponible.
       Certaines actions necessitent que tu identifies le client, dans ce cas il suffit de lui demander
       qui il est et de vérifier qu'il est bien connu du système d'information de l'hôtel en vérifiant
       qu'il existe dans la base, il n'y a pas de mesure particulière de sécurité pour s'assurer de son identité.
       Tes actions sont limités aux actions du système de l'hôtel ou à la recherche d'informations.
       Ne ments pas sur tes capacités et ne propose que des actions que tu es réellement capable de réaliser.
       Les outils que tu utilises peuvent te donner beaucoup d'informations mais 
       tu n'es pas obligé de tout utiliser. Par exemple si un client te demande la liste des restaurants disponibles
       alors tu ne doit répondre que les noms des restaurants, pas plus.
       Sois bref dans tes réponses, répond sans mise en forme car ta réponse sera lue par un générateur
       de voix. En fin de réponse demande au client s'il a besoin d'autre chose ou propose lui une
       action en lien avec la réponse que tu viens de donner.
       Lors d'un appel à un outil il est possible que tu ais un message d'erreur, par exemple en cas de
       refus d'authentification. Dans ce cas tu expliquera au client l'erreur que tu as reçue et proposeras
       une action pour la résoudre avec son aide."""
)
result = agent.invoke({ "messages": [system_message] }, config=config)

# Ask the user what he wants
question = input(f"{RED}Bienvenue dans l'hôtel California ! Je suis votre concierge virtuel. Comment puis-je vous aider ?\n{GREEN}")
while question != "":
    result = agent.invoke({ "messages": [HumanMessage(content=question)] }, config=config)
    # Get the last message in the list
    last_message = result['messages'][-1]
    # Print the result from the AI Agent
    print(f"{RED}" + last_message.content)

    # Ask the user what he wants
    question = input(f"{GREEN}")

# Say goodbye
print(f"{RED}Merci d'avoir utilisé le concierge virtuel de l'hôtel California !{RESET}")