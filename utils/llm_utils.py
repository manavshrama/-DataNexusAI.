from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import streamlit as st

def get_chat_response(messages, api_key, dataset_summary=""):
    """Gets a response from OpenAI using LangChain."""
    if not api_key:
        return "Please set your API key in Settings."
    
    chat = ChatOpenAI(openai_api_key=api_key, model="gpt-4-turbo-preview")
    
    system_prompt = f"""
    You are DataNexusAI, an expert data scientist. 
    You are helping a user analyze their dataset.
    Dataset context: {dataset_summary}
    Always be helpful, concise, and provide code or chart suggestions if appropriate.
    """
    
    langchain_messages = [SystemMessage(content=system_prompt)]
    for msg in messages:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        else:
            langchain_messages.append(AIMessage(content=msg["content"]))
            
    try:
        response = chat.invoke(langchain_messages)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"
