import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

load_dotenv()

openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

def embed_query(query):
    response = openai_client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=query
    )
    return response.data[0].embedding

def retrieve_documents(query, top_k=10):
    query_vector = embed_query(query)

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=top_k,
        fields="contentVector"
    )

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=["content", "source"],
        top=top_k
    )

    return list(results)

def rerank_documents(query, docs, top_n=3):
    rerank_prompt = f"""
You are a retrieval reranker.

Select the {top_n} most relevant document numbers for answering the question.

Question:
{query}

Documents:
"""

    for i, doc in enumerate(docs, start=1):
        rerank_prompt += f"\nDocument {i}:\nSource: {doc['source']}\nContent: {doc['content']}\n"

    response = openai_client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "Return only document numbers separated by commas. Example: 1,3,5"
            },
            {
                "role": "user",
                "content": rerank_prompt
            }
        ],
        temperature=0
    )

    selected_text = response.choices[0].message.content
    selected_indexes = []

    for item in selected_text.replace(" ", "").split(","):
        if item.isdigit():
            index = int(item) - 1
            if 0 <= index < len(docs):
                selected_indexes.append(index)

    reranked_docs = [docs[i] for i in selected_indexes]

    return reranked_docs[:top_n]

def generate_answer(query):
    docs = retrieve_documents(query, top_k=10)
    docs = rerank_documents(query, docs, top_n=3)

    context = "\n\n".join([
        f"Source: {doc['source']}\nContent: {doc['content']}"
        for doc in docs
    ])

    prompt = f"""
You are an enterprise AI assistant.

Answer ONLY using the retrieved context.

Rules:
- If the answer is not in the context, say:
  "I do not have enough information in the retrieved documents."
- Cite the source file name after every factual claim.
- Do not invent facts.
- Keep the answer clear and concise.

Question:
{query}

Retrieved Context:
{context}
"""

    response = openai_client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You are a grounded enterprise AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer, docs