from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document, HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import EMBEDDING_MODEL, MODEL_NAME, TOP_K
from prompts import HYDE_PROMPT, CRAG_PROMPT

import os

llm = ChatOpenAI(model=MODEL_NAME, temperature=0)



class Retriever:
    def __init__(self, path):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.db = self._load_db(path)

    def _load_db(self, path):
        docs = []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        for root, _, files in os.walk(path):
            for f in files:
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    text = file.read()
                    chunks = splitter.split_text(text)

                    for chunk in chunks:
                        docs.append(Document(page_content=chunk))

        return FAISS.from_documents(docs, self.embeddings)
    # -------- Retrieval Strategies -------- #

    def basic(self, query):
        return self.db.similarity_search(query, k=TOP_K)

    def multi_query(self, query):
        queries = [
            query,
            f"Explain: {query}",
            f"Help with: {query}"
        ]

        results = []
        for q in queries:
            results.extend(self.db.similarity_search(q, k=TOP_K))

        return self._dedupe(results)

    def hyde(self, query):
        hypo = llm.invoke([
            HumanMessage(content=HYDE_PROMPT.format(ticket=query))
        ]).content

        return self.db.similarity_search(hypo, k=TOP_K)

    # -------- CRAG -------- #

    def validate(self, query, docs):
        joined = "\n\n".join([d.page_content[:300] for d in docs])

        result = llm.invoke([
            HumanMessage(content=CRAG_PROMPT.format(
                question=query,
                docs=joined
            ))
        ]).content.strip().lower()

        return result == "good"

    # -------- Adaptive -------- #

    def retrieve(self, query):
        # heuristic
        if len(query.split()) < 5:
            docs = self.basic(query)
        elif "why" in query or "how" in query:
            docs = self.hyde(query)
        else:
            docs = self.multi_query(query)

        # # CRAG validation
        # if not self.validate(query, docs):
        #     docs = self.hyde(query)

        return self._dedupe(docs)

    def _dedupe(self, docs):
        seen = set()
        unique = []
        for d in docs:
            if d.page_content not in seen:
                unique.append(d)
                seen.add(d.page_content)
        return unique[:TOP_K]