from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage
from prompts import CONFIDENCE_PROMPT
from config import MODEL_NAME

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)


def compute_confidence(answer, docs):
    context = "\n\n".join([d.page_content[:300] for d in docs])

    response = llm.invoke([
        HumanMessage(content=CONFIDENCE_PROMPT.format(
            answer=answer,
            context=context
        ))
    ])

    try:
        return float(response.content.strip())
    except:
        return 0.0

def decide_escalation(classification, docs, answer, product):
    risk = classification.get("risk", "low")

    if risk == "high" and product != "visa":
        if not docs:
            return "escalated"

    # Visa → always reply (as per rules)
    if product == "visa":
        return "replied"

    # Only escalate if answer is clearly bad
    answer_lower = answer.lower()
    if "cannot determine" in answer_lower or "not enough information" in answer_lower:
        return "escalated"

    # Otherwise, reply
    return "replied"