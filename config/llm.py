import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set!")

# Main LLM for all agents
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    groq_api_key=API_KEY,
    max_tokens=2000,
)

# Fast LLM for quick operations
llm_fast = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    groq_api_key=API_KEY,
    max_tokens=1000,
)

# Creative LLM for planning/brainstorming
llm_creative = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=API_KEY,
    max_tokens=2500,
)
