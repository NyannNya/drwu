from langchain_openai import ChatOpenAI
from . import openai_api_key

def initialize_llm():
    llm = ChatOpenAI(
        openai_api_key=openai_api_key, 
        model="gpt-4o-mini"
    )
    llm.bind(response_format={"type": "json_object"})
    return llm