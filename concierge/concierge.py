import os
from dotenv import load_dotenv

# Get the environment variables
load_dotenv()

# Start a langchain chat session
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(base_url=os.getenv("LLM_API_URL"), openai_api_key=os.getenv("LLM_API_KEY"))

print("model created")

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

result = model.invoke(messages)

print("model response = ", result.content)
