# RAG Prototype with FastAPI

## Description
This is a Retrieval-Augmented Generation (RAG) prototype using FastAPI, FAISS, and an LLM. Users can upload documents and query them to get answers grounded in uploaded content.

## Setup
1. Create virtual environment
2. Install dependencies
3. Run FastAPI backend

## Usage
- Upload documents via `/upload-document`
- Query via `/query`
- Returns generated answer + source documents

## Architecture
[User Query] --> [FastAPI] --> [Vector Store: FAISS] --> [Retrieve Docs] --> [LLM Service] --> [Answer]
