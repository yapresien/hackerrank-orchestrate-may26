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

    # 🔥 RULE 1: Never escalate simple Visa/payment issues
    if product == "visa":
        return "replied"

    # 🔥 RULE 2: escalate only if high risk AND no docs
    if classification.get("risk") == "high" and not docs:
        return "escalated"

    # 🔥 RULE 3: escalate if answer truly cannot be determined
    if "cannot determine" in answer.lower() and not docs:
        return "escalated"

    # 🔥 RULE 4: otherwise always reply
    return "replied"