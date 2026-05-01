from classifier import classify_ticket
from router import route_ticket
from retriever import Retriever
from generator import generate_answer
from decision import decide_escalation
from config import DATA_PATH

retrievers = {
    "hackerrank": Retriever(f"{DATA_PATH}/hackerrank"),
    "claude": Retriever(f"{DATA_PATH}/claude"),
    "visa": Retriever(f"{DATA_PATH}/visa")
}


def process_ticket(ticket):

    classification = classify_ticket(ticket)
    route = route_ticket(ticket)

    retriever = retrievers[route]

    docs = retriever.retrieve(ticket)

    answer, justification = generate_answer(ticket, docs)

    status = decide_escalation(classification, docs, answer)

    if status == "escalated":
        return {
            "status": "escalated",
            "product_area": classification["product_area"],
            "response": "This issue requires review by a human support agent.",
            "justification": "Escalated due to low confidence or insufficient supporting evidence.",
            "request_type": classification["request_type"]
        }

    return {
        "status": "replied",
        "product_area": classification["product_area"],
        "response": answer,
        "justification": justification,
        "request_type": classification["request_type"]
    }