from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage
import json
from config import MODEL_NAME
from prompts import CLASSIFIER_PROMPT

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

def classify_ticket(ticket: str):
    response = llm.invoke([
        HumanMessage(content=CLASSIFIER_PROMPT.format(ticket=ticket))
    ])

    try:
        parsed = json.loads(response.content)
    except:
        parsed = {
            "request_type": "product_issue",
            "product_area": "general",
            "risk": "high"
        }

    # Force override invalid if ticket is long enough
    if parsed["request_type"] == "invalid" and len(ticket.strip()) > 15:
        parsed["request_type"] = "product_issue"

    return parsed