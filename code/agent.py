from classifier import classify_ticket
from router import route_ticket
from retriever import Retriever
from generator import generate_answer
from decision import decide_escalation
from config import DATA_PATH
from postprocess import post_process
from justifier import generate_justification
from config import DATA_PATH

RETRIEVERS = {
    "hackerrank": Retriever(f"{DATA_PATH}/hackerrank"),
    "claude": Retriever(f"{DATA_PATH}/claude"),
    "visa": Retriever(f"{DATA_PATH}/visa"),
}

def process_ticket(ticket: str):
    classification = classify_ticket(ticket)
    product = route_ticket(ticket)

    if product not in RETRIEVERS:
        print(f"[WARN] Unknown product: {product}")
        return None

    retriever = RETRIEVERS[product]
    docs = retriever.retrieve(ticket)

    answer, context = generate_answer(ticket, docs)
    status = decide_escalation(classification, docs, answer)
    justification = generate_justification(answer, docs)

    result = {
        "status": status,
        "product_area": classification["product_area"],
        "response": answer,
        "justification": justification,
        "request_type": classification["request_type"]
    }

    # ✅ POST-PROCESS HERE
    result = post_process(result)

    return result