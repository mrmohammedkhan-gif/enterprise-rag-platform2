import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())

tracer_provider = trace.get_tracer_provider()

tracer_provider.add_span_processor(
    SimpleSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
    )
)

OpenAIInstrumentor().instrument()




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

def retrieve_documents(query, top_k=5):
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

def generate_answer(query):
    docs = retrieve_documents(query)

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