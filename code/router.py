from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage

from prompts import ROUTER_PROMPT
from config import MODEL_NAME

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

def route_ticket(ticket: str):
    response = llm.invoke([
        HumanMessage(content=ROUTER_PROMPT.format(ticket=ticket))
    ])

    route = response.content.strip().lower()

    if route not in ["hackerrank", "claude", "visa"]:
        return "hackerrank"

    return route