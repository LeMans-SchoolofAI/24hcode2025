
# Load the langchain tools
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate




import os
from langchain.agents import initialize_agent, AgentType
# from langchain.chat_models import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory




"""Attention ce fichier ne foncitonne pas, il y a trop d'incompatibilité entre Gemini et Langchain. Le systemPrompt n'existe pas, mais plein d'autres 
fonctions non plus. Il faudrait revoir le code pour le rendre compatible avec Langchain. J'y ai déjà passé 5h.... Pierre """



MAX_DEPTH = 10

# Get the environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Langfuse handler
DEBUG_LANGFUSE = os.getenv("DEBUG_LANGFUSE", False)
if DEBUG_LANGFUSE:
    from langfuse.callback import CallbackHandler
    langfuse_handler = CallbackHandler(
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        host=os.getenv("LANGFUSE_HOST")
    )
    langfuse_handler.auth_check()
    # Use the handler directly if CallbackManager is not available
    callbacks = [langfuse_handler]
else:
    callbacks = []

# Define the tools
search_tool = DuckDuckGoSearchRun()

@tool
def dict_sujets() -> dict:
    """
    Retourne le dictionnaire des sujets des 24h du code 2025 avec le nom des porteurs en clé et le sujet en valeur
    """
    # Bouchon de test
    return {"HAUM":"lorep ipsum","Sopra Steria":"lorem fepeoi","Le Mans School of AI":"lorem opazdazdazdyc","ST Microelectronics":"patati patata"}

tools = [search_tool, Tool(name="dict_sujets", func=dict_sujets, description="Retourne le dictionnaire des sujets des 24h du code 2025.")]

SYSTEM_MESSAGE = """
Tu es un concierge virtuel pour l'événement les 24h du code.
Tu as des outils à ta disposition pour consulter les données liées à l'organisation de l'événement.
Quand un visiteur public demande une information, tu lui donnes la meilleure information disponible.
Certaines actions nécessitent que tu identifies le client, dans ce cas il suffit de lui demander
qui il est, il n'y a pas de mesure particulière de sécurité pour s'assurer de son identité.
Tes actions sont limités aux actions du système de l'organisation ou à la recherche d'informations.
Ne ment pas sur tes capacités et ne propose que des actions que tu es réellement capable de réaliser.
Les outils que tu utilises peuvent te donner beaucoup d'informations mais 
tu n'es pas obligé de tout utiliser.
Sois bref dans tes réponses, répond sans mise en forme car ta réponse sera lue par un générateur
de voix. Ne met aucun nombre écrit avec des chiffres, tu peux seulement en lettres. Par exemple 24 devient vingt-quatre.
Pareil pour les abréviations, par exemple 24h devient vingt-quatre heures.
En fin de réponse demande au visiteur s'il a besoin d'autre chose ou propose lui une
action en lien avec la réponse que tu viens de donner.
Lors d'un appel à un outil il est possible que tu ais un message d'erreur, par exemple en cas de
refus d'authentification. Dans ce cas tu expliquera au visiteur que tu as des soucis d'accès au
système d'information."""

agent = None
config = None

def reset_agent():
    global agent
    global config
    # Initialize Langfuse handler
    DEBUG_LANGFUSE = os.getenv("DEBUG_LANGFUSE", False)
    if DEBUG_LANGFUSE:
        from langfuse.callback import CallbackHandler
        langfuse_handler = CallbackHandler(
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            host=os.getenv("LANGFUSE_HOST")
        )
        langfuse_handler.auth_check()
        # Use the handler directly if CallbackManager is not available
        callbacks = [langfuse_handler]
    else:
        callbacks = []

    # Define the tools
    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool, Tool(name="dict_sujets", func=dict_sujets, description="Retourne le dictionnaire des sujets des 24h du code 2025.")]

    # Create the agent
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, max_retries=1, callbacks=callbacks)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        agent_kwargs={"system_message": SYSTEM_MESSAGE, "handle_parsing_errors": True}
    )
    return agent, config


def ask_AI(conversation_id, user_question=None, depth=0, reset=False):
    global agent
    global config
    if depth > MAX_DEPTH:
        return {'stop': True, "message" : "Maximum d'échanges atteint pour cette conversation"}
    
    if reset :
        agent, config = reset_agent()
        # config.update({"configurable": {"thread_id": f"conversation_{conversation_id}"}})
        return {'stop': False, "message": "Bienvenue aux vingt-quatre heures du code. Comment puis-je vous aider ?"}

    else:
        result = agent.run(user_question)
        return {'stop': False, "message": result['messages'][-1].content}

        
        
    

