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

def decide_escalation(classification, docs, answer):

    # No supporting documents → escalate
    if len(docs) == 0:
        return "escalated"

    # confidence = compute_confidence(answer, docs)
    # if confidence < 0.5:
    #     return "escalated"

    if "cannot determine" in answer.lower():
        return "escalated"

    # Otherwise reply
    return "replied"