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
DEBUG_LANGUSE = False
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
llm = ChatOpenAI(base_url=os.getenv("LLM_API_URL"), openai_api_key=os.getenv("LLM_API_KEY"))

print("llm created")

from pydantic import BaseModel, Field

# Note that the docstrings here are crucial, as they will be passed along
# to the model along with the class name.
class add(BaseModel):
    """Add two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

class multiply(BaseModel):
    """Multiply two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

tools = [add, multiply]
llm_with_tools = llm.bind_tools(tools)

# Execute query and parser result (Different from the first version)
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

query = "What is 3 * 12? Also, what is 11 + 49?"
chain = llm_with_tools | PydanticToolsParser(tools=tools)
result = chain.invoke(query)
print(result)

# Output:
# [multiply(a=3, b=12), add(a=11, b=49)]
