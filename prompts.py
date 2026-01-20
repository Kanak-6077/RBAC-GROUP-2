# backend/rag/prompts.py

SYSTEM_PROMPT = """
You are a helpful assistant for a Retrieval Augmented Generation (RAG) system.

RULES (VERY IMPORTANT):
1. Answer ONLY using the information provided in the CONTEXT.
2. If the answer is not present in the CONTEXT, say:
   "I do not have enough information in the provided documents."
3. Do NOT use any external knowledge.
4. Be clear, concise, and factual.
"""


def build_prompt(context_chunks: list, user_question: str) -> str:
    """
    Combines retrieved document chunks with user question
    to form the final prompt sent to the LLM.
    """

    context_text = "\n\n".join(context_chunks)

    final_prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context_text}

QUESTION:
{user_question}

ANSWER:
"""

    return final_prompt
