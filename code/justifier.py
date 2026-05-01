from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from prompts import JUSTIFICATION_PROMPT

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def generate_justification(answer, docs):
    if not docs:
        return "No relevant support documentation found."

    text = docs[0].page_content.lower()

    if "payment" in text or "card" in text:
        return "Based on support documentation describing payment disputes and issuer handling of transactions."

    if "access" in text or "workspace" in text:
        return "Based on support documentation describing workspace access control managed by administrators."

    if "test" in text or "submission" in text:
        return "Based on support documentation related to test submissions and evaluation policies."

    return "Based on relevant support documentation for the reported issue."