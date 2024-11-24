import os

# Load the langchain tools
from langchain_mistralai.chat_models import ChatMistralAI
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
    config = {"callbacks": [langfuse_handler]}
else:
    config = {}
# Create the agent
memory = MemorySaver()
#llm = ChatOpenAI(base_url=os.getenv("LLM_API_URL"), openai_api_key=os.getenv("LLM_API_KEY"))
#llm = ChatOllama(model="hf.co/nguyenthanhthuan/Llama_3.2_1B_Intruct_Tool_Calling_V2:latest")
llm = ChatMistralAI(model="mistral-large-latest", temperature=0, max_retries=2)

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

query = "To answer the question you should use a tool : what is 3 x 12 ?"
chain = llm_with_tools | PydanticToolsParser(tools=tools)
result = chain.invoke(query, config=config)
print(result)

# Output:
# [multiply(a=3, b=12), add(a=11, b=49)]
