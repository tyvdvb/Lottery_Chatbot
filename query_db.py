from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql.base import SQLDatabaseChain 

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    print("OpenAI API key not found")
    exit()

db = SQLDatabase.from_uri("sqlite:///lottery.db") 

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0, 
    openai_api_key=OPENAI_KEY) 

db_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    verbose=True
)

def ask_question(question: str) -> str:
    return db_chain.run(question)