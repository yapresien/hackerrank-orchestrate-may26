from classifier import classify_ticket
from router import route_ticket
from retriever import Retriever
from generator import generate_answer
from decision import decide_escalation
from config import DATA_PATH

mapping = {
    "payment": "payments",
    "billing": "payments",
    "transactions": "payments"
}

def post_process(result: dict) -> dict:

    # Product area normalization
    PRODUCT_AREA_MAP = {
        "payment": "payments",
        "payments": "payments",
        "billing": "payments",
        "transaction": "payments",
        "transactions": "payments",
        "card": "payments",
    }

    pa = result["product_area"].lower().strip()
    result["product_area"] = PRODUCT_AREA_MAP.get(pa, pa)
      
    # Clean response spacing
    result["response"] = result["response"].strip()
    if result["response"] == "":
        result["status"] = "escalated"
        result["response"] = "This issue requires review by a support agent."
    
    if "http" in result["response"]:
        result["response"] = result["response"].split("http")[0].strip()
    
    # Trim justification (keep it concise)
    result["justification"] = result["justification"].strip()

    # Optional: enforce max length
    if len(result["response"].split()) > 120:
        result["response"] = " ".join(result["response"].split()[:120])

    return result