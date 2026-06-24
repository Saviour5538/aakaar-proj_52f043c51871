from typing import List, Dict
from .embeddings import get_embedding
from .vector_store import VectorStore
from .llm_config import get_chat_client

def retrieve_context(query: str, top_k: int, session_id: str, user_id: str) -> List[Dict]:
    """
    Retrieve relevant context chunks for a given query.
    """
    vector_store = VectorStore()
    query_embedding = get_embedding([query])[0]
    results = vector_store.search(query_embedding, top_k, session_id=session_id, user_id=user_id)
    return results

def answer_question(query: str, session_id: str, user_id: str) -> Dict[str, object]:
    """
    Answer a question based on the user's documents.
    """
    context_matches = retrieve_context(query, top_k=5, session_id=session_id, user_id=user_id)
    context_texts = [match["metadata"]["chunk_text"] for match in context_matches]
    sources = [match["metadata"]["source"] for match in context_matches]

    prompt = (
        "You are an AI assistant. Answer the following question based on the provided context. "
        "If the answer is not in the context, say 'I don't know.'\n\n"
        "Context:\n" + "\n\n".join(context_texts) + "\n\n"
        "Question: " + query
    )

    client, model = get_chat_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}]
    )
    answer = response.choices[0].message.content

    return {"answer": answer, "sources": sources}