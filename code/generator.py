from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from prompts import GENERATION_PROMPT
from config import MODEL_NAME


# -----------------------------
# 🔹 Single LLM instance
# -----------------------------
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0
)


# -----------------------------
# 🔹 Answer Generation
# -----------------------------
def generate_answer(ticket, docs):
    if not docs:
        return "There is not enough context to provide a precise answer. Please contact support for further assistance."

    context = "\n\n".join([
        d.page_content.replace("[](", "").replace(")", "")
        for d in docs[:4]
    ])

    prompt = GENERATION_PROMPT.format(
        context=context,
        question=ticket
    )

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return response.content.strip()


# -----------------------------
# 🔹 Justification (deterministic)
# -----------------------------
def generate_justification(answer, docs):
    if not docs:
        return "No relevant context available."

    snippet = docs[0].page_content.strip().replace("\n", " ")[:120]
    return f"Answer based on retrieved documentation: {snippet}"