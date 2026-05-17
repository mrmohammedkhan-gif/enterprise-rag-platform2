import os
import uuid
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from pypdf import PdfReader

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

def read_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def read_file(path):
    if path.lower().endswith(".pdf"):
        return read_pdf(path)

    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def chunk_text(text, chunk_size=500, overlap=75):
    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def get_embedding(text):
    response = openai_client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=text
    )

    return response.data[0].embedding

documents = []

for filename in os.listdir("data"):
    path = os.path.join("data", filename)

    if not filename.lower().endswith((".txt", ".pdf")):
        continue

    text = read_file(path)
    chunks = chunk_text(text)

    for chunk in chunks:
        documents.append({
            "id": str(uuid.uuid4()),
            "content": chunk,
            "source": filename,
            "contentVector": get_embedding(chunk)
        })

search_client.upload_documents(documents)

print(f"Uploaded {len(documents)} chunks successfully")