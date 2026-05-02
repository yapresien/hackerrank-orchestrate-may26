from classifier import classify_ticket
from router import route_ticket
from retriever import Retriever
from generator import generate_answer, generate_justification
from decision import decide_escalation
from postprocess import post_process
from config import DATA_PATH


# -----------------------------
# 🔹 Initialize retrievers once
# -----------------------------
RETRIEVERS = {
    "hackerrank": Retriever(f"{DATA_PATH}/hackerrank"),
    "claude": Retriever(f"{DATA_PATH}/claude"),
    "visa": Retriever(f"{DATA_PATH}/visa"),
}


# -----------------------------
# 🔹 Main pipeline
# -----------------------------
def process_ticket(ticket: str):
    try:
        # -------------------------
        # 1. Classification
        # -------------------------
        classification = classify_ticket(ticket)
        request_type = classification.get("request_type", "product_issue")
        product_area = classification.get("product_area", "general")
        risk = classification.get("risk", "low")

        # -------------------------
        # 2. Routing
        # -------------------------
        product = route_ticket(ticket)

        if product not in RETRIEVERS:
            return _escalation_fallback(
                product_area,
                request_type,
                reason="Unknown product routing"
            )

        retriever = RETRIEVERS[product]

        # -------------------------
        # 3. Retrieval
        # -------------------------
        docs = retriever.retrieve(ticket)[:4]

        # Hard fail if no docs → prevents hallucination
        if not docs:
            return _escalation_fallback(
                product_area,
                request_type,
                reason="No supporting documents"
            )

        # -------------------------
        # 4. Generation
        # -------------------------
        answer = generate_answer(ticket, docs)

        if isinstance(answer, tuple):
            answer = answer[0]

        answer = answer.strip()

        # -------------------------
        # 5. Escalation decision
        # -------------------------
        status = decide_escalation(
            classification,
            docs,
            answer,
            product
        )

        # -------------------------
        # 6. Justification
        # -------------------------
        if status == "replied":
            justification = generate_justification(answer, docs)
        else:
            justification = "Escalated due to insufficient or high-risk context."
        
        if status == "escalated":
            answer = "I’m unable to fully resolve this based on available information. Please contact the appropriate support team or your service provider for further assistance."
        
        # -------------------------
        # 7. Final output
        # -------------------------
        result = {
            "status": status,
            "product_area": product_area,
            "response": answer,
            "justification": justification,
            "request_type": request_type
        }

        # -------------------------
        # 8. Post-processing
        # -------------------------
        result = post_process(result)

        return result

    except Exception as e:
        print(f"[ERROR] {e}")
        return _escalation_fallback(
            product_area="unknown",
            request_type="product_issue",
            reason=str(e)
        )


# -----------------------------
# 🔹 Safe fallback
# -----------------------------
def _escalation_fallback(product_area, request_type, reason=""):
    return {
        "status": "escalated",
        "product_area": product_area,
        "response": "This issue requires review by a human support agent.",
        "justification": f"Escalated due to: {reason}",
        "request_type": request_type
    }