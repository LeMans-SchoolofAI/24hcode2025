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

@tool
def list_restaurants() -> [str]:
    """Retourne la liste des restaurants de l'hotel avec les informations suivantes :
       - id technique
       - nom
       - description
       - capacité
       - horaires d'ouverture
       - emplacement
       """
    # Access the API to get the list of hotels
    url = f"{HOTEL_API_URL}/restaurants"
    headers = {"Authorization": f"{HOTEL_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return ("Accès refusé par l'API")
    data = response.json()
    # Return the list of hotels
    return (data)


tools = [search_tool, list_restaurants]


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
       qui il est, il n'y a pas de mesure particulière de sécurité pour s'assurer de son identité.
       Tes actions sont limités aux actions du système de l'hôtel ou à la recherche d'informations.
       Ne ments pas sur tes capacités et ne propose que des actions que tu es réellement capable de réaliser.
       Les outils que tu utilises peuvent te donner beaucoup d'informations mais 
       tu n'es pas obligé de tout utiliser. Par exemple si un client te demande la liste des restaurants disponibles
       alors tu ne doit répondre que les noms des restaurants, pas plus.
       Sois bref dans tes réponses, répond sans mise en forme car ta réponse sera lue par un générateur
       de voix. En fin de réponse demande au client s'il a besoin d'autre chose ou propose lui une
       action en lien avec la réponse que tu viens de donner.
       Lors d'un appel à un outil il est possible que tu ais un message d'erreur, par exemple en cas de
       refus d'authentification. Dans ce cas tu expliquera au client que tu as des soucis d'accès au
       système d'information."""
)
result = agent.invoke({ "messages": [system_message] }, config=config)

# Ask the user what he wants
question = input("Comment puis-je vous aider ? ")
while question != "":
    result = agent.invoke({ "messages": [HumanMessage(content=question)] }, config=config)
    # Get the last message in the list
    last_message = result['messages'][-1]
    # Print the result from the AI Agent
    print(last_message.content)

    # Ask the user what he wants
    question = input("")

# Say goodbye
print("Goodbye")