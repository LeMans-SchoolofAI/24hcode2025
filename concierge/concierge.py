import os

# Load the langchain tools
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Get the environment variables
from dotenv import load_dotenv
load_dotenv()

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

# Create the agent
memory = MemorySaver()
model = ChatOpenAI(base_url=os.getenv("LLM_API_URL"), openai_api_key=os.getenv("LLM_API_KEY"))
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

print("agent created")

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
if DEBUG_LANGUSE:
    config["callbacks"] = ([langfuse_handler])
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in sf, whats name of the mayor here ?")]}, config
):
    print(chunk)
    print("----")

