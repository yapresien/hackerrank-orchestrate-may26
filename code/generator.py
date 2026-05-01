from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage
from prompts import GENERATION_PROMPT, JUSTIFICATION_PROMPT
from config import MODEL_NAME

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)


def generate_answer(ticket, docs):
    context = "\n\n".join([d.page_content[:500] for d in docs])

    answer = llm.invoke([
        HumanMessage(content=GENERATION_PROMPT.format(
            context=context,
            question=ticket
        ))
    ]).content

    justification = llm.invoke([
        HumanMessage(content=JUSTIFICATION_PROMPT.format(
            answer=answer,
            context=context
        ))
    ]).content

    return answer, justification