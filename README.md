# Enterprise RAG Evaluation & Observability Platform

A Streamlit-based enterprise Retrieval-Augmented Generation platform built with Azure OpenAI, Azure AI Search, vector embeddings, PDF ingestion, and grounded response generation.

## Features

- Azure OpenAI chat integration
- Azure OpenAI embeddings
- Azure AI Search vector retrieval
- Hybrid keyword + vector search
- PDF and TXT document ingestion
- Streamlit chat interface
- Retrieved context transparency
- Grounded answers with source citations
- Hallucination-resistant prompt design
- Evaluation script for retrieval testing

## Tech Stack

Python  
Streamlit  
Azure OpenAI  
Azure AI Search  
Azure Blob Storage  
Vector Embeddings  
PDF Processing  

## Architecture

```text
User Question
   ↓
Streamlit App
   ↓
Azure OpenAI Embedding
   ↓
Azure AI Search Vector Retrieval
   ↓
Retrieved Context
   ↓
Azure OpenAI Chat Completion
   ↓
Grounded Answer + Sources