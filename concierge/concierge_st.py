import os
import requests
import uuid
import streamlit as st

# Load the langchain tools
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
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

# Initialize Langfuse handler
DEBUG_LANGFUSE = True
# Generate a random session ID
session_id = str(uuid.uuid4())
if DEBUG_LANGFUSE:
    try:
        from langfuse.callback import CallbackHandler
        langfuse_handler = CallbackHandler(
            secret_key=os.getenv("LANG_FUSE_SECRET_KEY"),
            public_key=os.getenv("LANG_FUSE_PUBLIC_KEY"),
            host=os.getenv("LANG_FUSE_HOST"),
            session_id=session_id
        )
        langfuse_handler.auth_check()
        config = {"callbacks": [langfuse_handler]}
    except Exception as e:
        print(f"Error initializing Langfuse handler: {e}")
        config = {}
else:
    config = {}

# Define the tools
search_tool = DuckDuckGoSearchRun()

def create_llm():
    provider = os.getenv("LLM_PROVIDER", "Mistral")
    if provider == "Mistral":
        llm = ChatMistralAI(model="mistral-large-latest", temperature=0, max_retries=2, )
    elif provider == "Google":
        key_file = os.getenv("GOOGLE_API_KEY")
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=key_file, temperature=0, max_retries=2)
    return llm

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
    return (data)

@tool
def search_clients(search_term: str, page: int = 1) -> [str]:
    """
    Effectue une recherche sur les clients de l'hôtel par le nom ou le numéro de téléphone

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
    url = f"{HOTEL_API_URL}/clients/?search={search_term}&page={page}"
    response = requests.get(url, headers=get_headers())
    try:
        data = response.json()
    except:
        data = response
    return (data)

@tool
def get_client_info(id_client: str) -> [str]:
    """
    Retourne les informations d'un client

    Args:
        id_client (str): id technique du client

    Returns:
        id (str): id technique du client
        name (str): nom et prénom du client
        phone_number (str): numéro de téléphone
        room_number (str): numéro de chambre
        special_requests (str): demandes spéciales
    """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/clients/{id_client}/"
    response = requests.get(url, headers=get_headers())
    try:
        data = response.json()
    except:
        data = response
    return (data)

@tool
def update_client(id_client: str, name: str=None, phone_number: str=None,
                  room_number: str=None, special_requests: str=None) -> [str]:
    """
    Mise à jour d'un client

    Args:
        id_client (str): id technique du client
        name (str): nom et prénom du client (optionnel)
        phone_number (str): numéro de telephone (optionnel)
        room_number (str): numéro de chambre (optionnel)
        special_requests (str):demandes speciales (optionnel)
    """
    url = f"{HOTEL_API_URL}/clients/{id_client}/"
    params = {
        "name": name,
        "phone_number": phone_number,
        "room_number": room_number,
        "special_requests": special_requests
    }
    filtered_params = {k: v for k, v in params.items() if v is not None}
    response = requests.put(url, headers=get_headers(), json=filtered_params)
    try:
        data = response.json()
    except:
        data = response
    return (data)

@tool
def delete_client(id_client: str) -> [str]:
    """
    Suppression d'un client

    Args:
        id_client (str): id technique du client
    """
    url = f"{HOTEL_API_URL}/clients/{id_client}/"
    response = requests.delete(url, headers=get_headers())
    try:
        data = response.json()
    except:
        data = response
    return (data)

@tool
def create_client(name: str, phone_number: str, room_number: str, special_requests: str) -> [str]:
    """
    Création d'un nouveau client

    Args:
        name (str): nom et prénom du client
        phone_number (str): numéro de téléphone
        room_number (str): numéro de chambre
        special_requests (str): demandes spéciales
    
    Returns:
        id (str): id technique du client
    """
    url = f"{HOTEL_API_URL}/clients/"
    response = requests.post(url, headers=get_headers(), json={"name": name, "phone_number": phone_number,
                             "room_number": room_number, "special_requests": special_requests})
    try:
        data = response.json()
    except:
        data = response
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
                      id_restaurant: str = None, id_client: str = None, page: int = 1) -> [str]:
    """
    Retourne la liste des reservations qui répondent aux critères
    
    Args:
        date_from (str): date de debut de la reservation (au format YYYY-MM-DD)
        date_to (str): date de fin de la reservation (au format YYYY-MM-DD)
        id_meal (str): l'id du type de repas (disponible dans la liste des repas)
        id_restaurant (str): l'id du restaurant (disponible dans la liste des restaurants)
        id_client (str): l'id du client (disponible dans la liste des clients)
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
        "client": id_client,
        "page": page
    }
    filtered_params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, headers=get_headers(), params=filtered_params)
    try:
        data = response.json()
    except:
        data = response
    return (data)

@tool
def make_reservation(client: str, restaurant: str, date: str, meal: str, number_of_guests: int, special_requests: str) -> [str]:
    """
    Prend une réservation dans l'un des restaurants de l'hôtel.
    Attention à ce que le type de repas soit compatible avec l'horaire d'ouverture du restaurant
    
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
    return (data)

@tool
def modify_reservation(id_reservation: str, id_client: str = None, id_restaurant: str = None, date: str = None,
                       id_meal: str = None, number_of_guests: int = None, special_requests: str = None) -> [str]:
    """
    Modifie une reservation existante
    Attention à ce que le type de repas soit compatible avec l'horaire d'ouverture du restaurant

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
    return (data)

@tool
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
    return (data)

tools = [search_tool, list_restaurants, search_clients, get_client_info, update_client, delete_client,
        create_client, list_meals, list_reservations, make_reservation, modify_reservation, delete_reservation]

# Use the agent
# Define a thread_id to track the conversation
config.update({"configurable": {"thread_id": "abc123"}})

# Define the system message and give the agent some context
system_message = SystemMessage(content=
    """Tu es un concierge virtuel pour l'hôtel California. L'hôtel est situé dans la ville du Mans, en France.
       Tu as des outils à ta disposition pour consulter les données de l'hôtel et agir avec le système de l'hôtel.
       Quand un client demande une information, tu lui donne la meilleure information disponible.
       Lorsque tu discutes avec le client tu n'utilses pas l'id des enregistrements de la base de données mais tu
       utilises le nom ou la description selon le besoin.
       Certaines actions necessitent que tu identifies le client, dans ce cas il suffit de lui demander
       qui il est et de vérifier qu'il est bien connu du système d'information de l'hôtel en vérifiant
       qu'il existe dans la base, il n'y a pas de mesure particulière de sécurité pour s'assurer de son identité.
       Tes actions sont limités aux actions du système de l'hôtel ou à la recherche d'informations.
       Ne ments pas sur tes capacités et ne propose que des actions que tu es réellement capable de réaliser.
       Les outils que tu utilises peuvent te donner beaucoup d'informations mais 
       tu n'es pas obligé de tout utiliser. Par exemple si un client te demande la liste des restaurants disponibles
       alors tu ne peux répondre en ne fournissant que les noms des restaurants, il n'est pas nécessaire de
       détailler si le client ne l'a pas demandé.
       D'une manière générale sois bref dans tes réponses et répond sans mise en forme car ta réponse sera lue par un
       générateur de voix. En fin de réponse demande au client s'il a besoin d'autre chose ou propose lui une
       action en lien avec la réponse que tu viens de donner.
       Lors d'un appel à un outil il est possible que tu ais un message d'erreur, par exemple en cas de
       refus d'authentification. Dans ce cas tu expliquera au client l'erreur que tu as reçue et proposeras
       une action pour la résoudre avec son aide.
       Soit attentif quand tu prends ou modifies des réservations pour les restaurants. Les horaires d'ouverture des restaurants
       sont à prendre en compte car certains ne permettent pas de prendre tous les types de repas. Il n'est pas non plus
       autorisé pour un client de prendre plusieurs réservations au même moment. Dans ce cas il est souhaitable que tu
       consulte préalablement les réservations de ce client avant d'enregistrer ou modifier une réservation et ainsi
       éviter des conflits."""
)

# Create the agent, including the system message
memory = MemorySaver()
llm = create_llm()
agent = create_react_agent(llm, tools, state_modifier=system_message, checkpointer=memory)

# ----------------- STREAMLIT APP CODE STARTS HERE -----------------

# Set page configuration
st.set_page_config(
    page_title="Hotel California Virtual Concierge",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Add agent in streamlit state
if "agent" not in st.session_state:
    st.session_state.agent = agent

# Add custom CSS for styling
st.markdown("""
<style>
.hotel-title {
    color: white;
    background-color: #1a5276;
    padding: 20px;
    text-align: center;
    border-radius: 5px;
    margin-bottom: 20px;
}
.stTextInput > div > div > input {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# Hotel header
st.markdown("<h1 class='hotel-title'>HOTEL CALIFORNIA</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Concierge Virtuel</h3>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bienvenue dans l'hôtel California ! Je suis votre concierge virtuel. Comment puis-je vous aider ?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Comment puis-je vous aider ?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("En train de réfléchir..."):
            # Process with your existing agent
            result = st.session_state.agent.invoke({"messages": [HumanMessage(content=prompt)]}, config=config)
            last_message = result['messages'][-1]
            response = last_message.content
            st.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© Hotel California - Le Mans, France</p>", unsafe_allow_html=True)