# Enterprise RAG Evaluation & Observability Platform

An enterprise Retrieval-Augmented Generation (RAG) application built with Azure OpenAI, Azure AI Search, vector embeddings, PDF ingestion, and Streamlit.

The platform retrieves enterprise documents, generates grounded answers, and exposes retrieved context for transparency and evaluation.

## Key Features

- Azure OpenAI chat completion
- Azure OpenAI embeddings
- Azure AI Search vector retrieval
- Hybrid keyword + vector search
- PDF and TXT document ingestion
- Streamlit chat interface
- Retrieved context transparency
- Grounded responses with source citations
- Hallucination-resistant prompt design
- Retrieval evaluation workflow
- Azure Blob Storage ingestion support

## Architecture

```text
User Question
   ↓
Streamlit App
   ↓
Azure OpenAI Embedding Model
   ↓
Azure AI Search Vector + Hybrid Retrieval
   ↓
Retrieved Document Chunks
   ↓
Azure OpenAI Chat Model
   ↓
Grounded Answer + Sources