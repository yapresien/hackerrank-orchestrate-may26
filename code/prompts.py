CLASSIFIER_PROMPT = """
Classify the support ticket.

Return STRICT JSON ONLY (no explanation, no extra text):
{{
  "request_type": "product_issue | feature_request | bug | invalid",
  "product_area": "...",
  "risk": "low | high"
}}

Rules:
- Instead of "likely": "The cause is..."
- Instead of "seems": "This happens when..."
- bug = system malfunction, crashes, platform errors
- product_issue = payment problems, login issues, transaction failures, access problems, account issues
- feature_request = asking for new functionality or improvements
- invalid = unclear, spam, off-topic, or not actionable (e.g., personal requests for score changes)
- high risk = payment issues, account security, billing errors, access revocations

Use short, consistent labels for product_area (e.g., "access", "login", "payments", "billing", "account").

Ticket:
{ticket}
"""

ROUTER_PROMPT = """
Which product does this ticket belong to?

- hackerrank: for coding tests, interviews, assessments
- claude: for AI assistant, workspace, Anthropic services
- visa: for credit cards, payments, transactions, merchants

Return ONLY the product name (lowercase).
Ticket: {ticket}
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
- Explain ONLY what is explicitly supported by the context
- Do NOT infer reasons not stated in the documentation
- Provide specific resolution steps
- Be concise and specific (max ~100 words)
- Do NOT invent policies, phone numbers, email addresses, URLs, or external links
- Do NOT instruct the user to call or contact via phone unless explicitly stated in the context
- Do NOT ask the user for additional information
- NEVER use words like "likely", "may", "could", "might", or "seems"
- Use "This happens when..." for issues or errors
- Use direct statements for policies (do NOT force "The cause is")
- If the context is insufficient, say you cannot determine the answer

If the issue involves payments, mention authorization holds ONLY if clearly relevant.

Write the answer as a natural paragraph.

Context:
{context}

Question:
{question}

Answer:
"""

JUSTIFICATION_PROMPT = """
Provide a concise justification (1 sentence) referencing support documentation and the type of issue.
Return ONE sentence explaining WHY the answer is correct.
Reference the specific concept (e.g., authorization holds, admin access, issuer handling).
Do NOT be generic.
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