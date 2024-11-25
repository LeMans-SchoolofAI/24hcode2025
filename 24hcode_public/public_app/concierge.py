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

MAX_DEPTH = 10

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
    config = {"callbacks": [langfuse_handler]}
else:
    config = {}

# Define the tools
search_tool = DuckDuckGoSearchRun()

@tool
def dict_sujets() -> [dict]:
    """
    Retourne le dictionnaire des sujets des 24h du code 2025 avec le nom des porteurs en clé et le sujet en valeur
    """
    
    # Bouchon de test
    return {"HAUM":"lorep ipsum","Sopra Steria":"lorem fepeoi","Le Mans School of AI":"lorem opazdazdazdyc","ST Microelectronics":"patati patata"}
    # # Access the API to get the list of hotels
    # url = f"{HOTEL_API_URL}/restaurants"
    # headers = {"Authorization": f"{HOTEL_API_TOKEN}"}
    # response = requests.get(url, headers=headers)
    # if response.status_code != 200:
    #     return ("Accès refusé par l'API")
    # data = response.json()
    # # Return the list of hotels
    # return (data)


tools = [search_tool, dict_sujets]


# Create the agent
memory = MemorySaver()
llm = ChatMistralAI(model="mistral-large-latest", temperature=0, max_retries=1)



# def tchat(context=None, depth=0):
#     if depth > MAX_DEPTH:
#         print("Maximum d'échanges atteint pour cette conversation")
#         return 
    
#     if context == None:
#         agent = create_react_agent(llm, tools, checkpointer=memory)

#         # Use the agent
#         # Define a thread_id to track the conversation
#         config.update({"configurable": {"thread_id": "abc123"}})

#         # Define the system message and give the agent some context
#         system_message = SystemMessage(content=
#             """Tu es un concierge virtuel pour l'événement les 24h du code'.
#             Tu as des outils à ta disposition pour consulter les données liées à l'ogranisation de l'événement.
#             Quand un visiteur public demande une information, tu lui donnes la meilleure information disponible.
#             Certaines actions necessitent que tu identifies le client, dans ce cas il suffit de lui demander
#             qui il est, il n'y a pas de mesure particulière de sécurité pour s'assurer de son identité.
#             Tes actions sont limités aux actions du système de l'organisation ou à la recherche d'informations.
#             Ne ments pas sur tes capacités et ne propose que des actions que tu es réellement capable de réaliser.
#             Les outils que tu utilises peuvent te donner beaucoup d'informations mais 
#             tu n'es pas obligé de tout utiliser.
#             Sois bref dans tes réponses, répond sans mise en forme car ta réponse sera lue par un générateur
#             de voix. En fin de réponse demande au visiteur s'il a besoin d'autre chose ou propose lui une
#             action en lien avec la réponse que tu viens de donner.
#             Lors d'un appel à un outil il est possible que tu ais un message d'erreur, par exemple en cas de
#             refus d'authentification. Dans ce cas tu expliquera au visiteur que tu as des soucis d'accès au
#             système d'information."""
#         )
#         result = agent.invoke({ "messages": [system_message] }, config=config)
        
#         # Ask the user what he wants
#         question = input("Comment puis-je vous aider ? ")
#     else:
#         agent = context['agent']
#         config = context['config']
#         question = input()
    
#     if question == "":
#         return
     
#     # Ask the AI Agent
#     result = agent.invoke({ "messages": [HumanMessage(content=question)] }, config=config)
#     # Get the last message in the list
#     last_message = result['messages'][-1]
#     # Print the result from the AI Agent
#     print(last_message.content)

#     tchat({"agent": agent, "config": config}, depth+1)





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
        config = {"callbacks": [langfuse_handler]}
    else:
        config = {}

    # Define the tools
    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool, dict_sujets]

    # Create the agent
    memory = MemorySaver()
    llm = ChatMistralAI(model="mistral-large-latest", temperature=0, max_retries=1)
    agent = create_react_agent(llm, tools, checkpointer=memory)
    return agent, config
    

def ask_AI(conversation_id, user_question=None, depth=0, reset=False):
    global agent
    global config
    if depth > MAX_DEPTH:
        return {'stop': True, "message" : "Maximum d'échanges atteint pour cette conversation"}
    
    if reset :
        agent, config = reset_agent()
        config.update({"configurable": {"thread_id": f"conversation_{conversation_id}"}})

        # Define the system message and give the agent some context
        system_message = SystemMessage(content=
            """Tu es un concierge virtuel pour l'événement les 24h du code'.
            Tu as des outils à ta disposition pour consulter les données liées à l'ogranisation de l'événement.
            Quand un visiteur public demande une information, tu lui donnes la meilleure information disponible.
            Certaines actions necessitent que tu identifies le client, dans ce cas il suffit de lui demander
            qui il est, il n'y a pas de mesure particulière de sécurité pour s'assurer de son identité.
            Tes actions sont limités aux actions du système de l'organisation ou à la recherche d'informations.
            Ne ments pas sur tes capacités et ne propose que des actions que tu es réellement capable de réaliser.
            Les outils que tu utilises peuvent te donner beaucoup d'informations mais 
            tu n'es pas obligé de tout utiliser.
            Sois bref dans tes réponses, répond sans mise en forme car ta réponse sera lue par un générateur
            de voix. En fin de réponse demande au visiteur s'il a besoin d'autre chose ou propose lui une
            action en lien avec la réponse que tu viens de donner.
            Lors d'un appel à un outil il est possible que tu ais un message d'erreur, par exemple en cas de
            refus d'authentification. Dans ce cas tu expliquera au visiteur que tu as des soucis d'accès au
            système d'information."""
        )
        result = agent.invoke({ "messages": [system_message] }, config=config)
        return {'stop': False, "message": "Bienvenue aux 24h du code. Comment puis-je vous aider ?"}
    
    else:
        result = agent.invoke({ "messages": [HumanMessage(content=user_question)] }, config=config)
        return {'stop': False, "message": result['messages'][-1].content}
        
        
    

