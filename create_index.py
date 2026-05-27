import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

client = SearchIndexClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

try:
    client.delete_index(index_name)
    print(f"Deleted existing index: {index_name}")
except ResourceNotFoundError:
    print("No existing index found.")

fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SearchableField(name="source", type=SearchFieldDataType.String),
    SearchField(
        name="contentVector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="vector-profile"
    )
]

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(name="hnsw-config")
    ],
    profiles=[
        VectorSearchProfile(
            name="vector-profile",
            algorithm_configuration_name="hnsw-config"
        )
    ]
)

index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search
)

client.create_index(index)

print("Created Azure AI Search index with 1536 vector dimensions")