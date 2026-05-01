CLASSIFIER_PROMPT = """
Classify the support ticket.

Return STRICT JSON:
{
  "request_type": "product_issue | feature_request | bug | invalid",
  "product_area": "...",
  "risk": "low | high"
}

Rules:
- "bug" = system malfunction
- "feature_request" = asking for new functionality
- "invalid" = unclear / not actionable

Ticket:
{ticket}
"""

ROUTER_PROMPT = """
Which product does this belong to?

Options:
- hackerrank (coding platform, submissions, tests)
- claude (AI assistant usage, billing, prompts)
- visa (payments, cards, transactions)

Return ONLY one word.

Ticket:
{ticket}
"""

HYDE_PROMPT = """
Write a detailed support answer that would correctly resolve this issue.

Ticket:
{ticket}

Answer:
"""

CRAG_PROMPT = """
Evaluate if the retrieved documents are sufficient to answer the question.

Question:
{question}

Documents:
{docs}

Return:
- "good" if sufficient
- "bad" if irrelevant or insufficient
"""

GENERATION_PROMPT = """
You are a support agent.

STRICT RULES:
- Use ONLY the provided context
- If unsure → say you cannot determine
- Do NOT invent policies

Context:
{context}

Question:
{question}

Answer:
"""

JUSTIFICATION_PROMPT = """
Explain briefly why this answer is correct using the context.

Answer:
{answer}

Context:
{context}
"""

CONFIDENCE_PROMPT = """
Rate confidence in this answer.

Answer:
{answer}

Context:
{context}

Return a number between 0 and 1.
"""