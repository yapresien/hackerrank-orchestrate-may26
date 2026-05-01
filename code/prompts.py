CLASSIFIER_PROMPT = """
Classify the support ticket.

Return STRICT JSON ONLY (no explanation, no extra text):
{{
  "request_type": "product_issue | feature_request | bug | invalid",
  "product_area": "...",
  "risk": "low | high"
}}

Rules:
- bug = system malfunction (platform error, crash)
- product_issue = payment problems, login issues, transaction failures
- feature_request = asking for new functionality
- invalid = unclear, spam, or not actionable
- high risk = payment issues, account security, billing errors

Use short, consistent labels for product_area (e.g., "payments", "login", "billing").

Ticket:
{ticket}
"""

ROUTER_PROMPT = """
Which product does this belong to?

Options:
- hackerrank
- claude
- visa

Return ONLY one word from the options above (lowercase, no explanation).

Ticket:
{ticket}
"""

HYDE_PROMPT = """
Write a detailed, realistic support answer that would resolve this issue.
Do not include policies not commonly found in support documentation.

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

Return ONLY one word:
- good (relevant and sufficient)
- bad (irrelevant or insufficient)
"""

GENERATION_PROMPT = """
You are a support agent.

RULES:
- Use ONLY the provided context
- Briefly explain the likely cause
- Provide clear next steps
- Be concise and specific (max ~100 words)
- Do NOT invent policies or include external links

If the issue involves payments, mention authorization holds when relevant.

Write the answer as a natural paragraph.

Context:
{context}

Question:
{question}

Answer:
"""

JUSTIFICATION_PROMPT = """
Provide a concise justification (1 sentence) referencing the support documentation.

Answer:
{answer}

Context:
{context}
"""

CONFIDENCE_PROMPT = """
Rate confidence in this answer based on the context.

Answer:
{answer}

Context:
{context}

Return ONLY a number between 0 and 1.
"""