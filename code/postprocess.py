import re

SAFE_FALLBACK_RESPONSE = "This issue requires review by a human support agent."
ALLOWED_AREAS = {
    "payments", "billing", "access", "login", "hiring", "submission", "account"
}
AREA_MAP = {
    "payment": "payments",
    "billing": "payments",
    "transaction": "payments",
    "transactions": "payments",
    "card": "payments",
    "access": "access",
    "login": "access",
    "signin": "access",
    "authentication": "access",
    "auth": "access",
    "security": "account",
    "infosec": "account",
    "connectivity": "account",
    "resume_builder": "account",
    "interview_management": "account",
    "aws_bedrock": "account",
    "lti": "account",
    "n/a": "account",
    "": "account",
}

VAGUE_PATTERNS = [
    (r"\bIt seems\b", "The issue is"),
    (r"\bThe likely cause\b", "The cause"),
    (r"\blikely due to\b", "due to"),
    (r"\blikely\b", ""),
    (r"\bmay be\b", "is"),
    (r"\bcould be\b", "is"),
    (r"\bmight be\b", "is"),
    (r"\bprobably\b", "is"),
]

BANNED_CONTACT_PATTERNS = [
    r"\+?\d[\d\-\s]{7,}",
    r"\b\w+@\w+\.\w+\b",
    r"https?://[\w\.-]+",
    r"http://[\w\.-]+",
]

BANNED_COMPANY_WORDS = ["Interpayment", "Ltd", "Inc"]


def clean_response(text):
    response = text.strip()

    for pattern, replacement in VAGUE_PATTERNS:
        response = re.sub(pattern, replacement, response, flags=re.IGNORECASE)

    for banned in BANNED_COMPANY_WORDS:
        response = re.sub(rf"\b{re.escape(banned)}\b", "", response)

    response = re.sub(r'https?://[^\s]+', "", response)
    response = re.sub(r"\b\w+@\w+\.\w+\b", "support", response)
    response = re.sub(r"\+?\d[\d\-\s]{7,}", "", response)
    response = re.sub(r"\b(call|contact|email)\b[^\.]*\+?\d[\d\-\s]{4,}", "", response, flags=re.IGNORECASE)
    response = re.sub(r"\s+", " ", response).strip()

    return response


def normalize_product_area(area: str) -> str:
    pa = area.lower().strip()
    normalized = AREA_MAP.get(pa, pa)
    return normalized if normalized in ALLOWED_AREAS else "account"


def detect_unsafe_response(text: str) -> bool:
    if not text:
        return True

    lowered = text.lower()

    # ONLY escalate if totally useless
    if "cannot determine" in lowered:
        return True

    return False


def post_process(result):
    result["product_area"] = normalize_product_area(result.get("product_area", "account"))

    result["response"] = clean_response(result.get("response", ""))
    result["justification"] = result.get("justification", "").strip()

    if detect_unsafe_response(result["response"]):
        result["status"] = "escalated"
        result["response"] = SAFE_FALLBACK_RESPONSE
        result["justification"] = "Escalated due to unsafe or insufficient response content."

    if result["status"] not in ["replied", "escalated"]:
        result["status"] = "escalated"

    # force minimum answer quality
    if result["status"] == "replied" and len(result["response"]) < 40:
        result["status"] = "escalated"

    if result["request_type"] not in ["product_issue", "feature_request", "bug", "invalid"]:
        result["request_type"] = "product_issue"

    if not result["response"]:
        result["status"] = "escalated"
        result["response"] = SAFE_FALLBACK_RESPONSE
        result["justification"] = "Escalated because the response was empty after cleanup."

    return result