from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from prompts import JUSTIFICATION_PROMPT

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# def generate_justification(answer, docs):
#     context = "\n\n".join([d.page_content for d in docs[:3]])

#     prompt = JUSTIFICATION_PROMPT.format(
#         answer=answer,
#         context=context
#     )

#     response = llm([HumanMessage(content=prompt)])

#     return response.content.strip()
def generate_justification(answer, docs):
    if not docs:
        return "No relevant context found."

    return "Based on retrieved support documentation related to the issue."