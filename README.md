# F1 Regs AI
 
An AI-powered chatbot that answers questions about FIA Formula 1 regulations using Retrieval-Augmented Generation (RAG). Built from scratch with Python and ChromaDB — no frameworks — to deeply understand the RAG pipeline, then refactored with LangChain for comparison.
 
> **Why F1 regulations?** LLMs can't reliably answer detailed questions about specific regulation clauses, minimum car weights, or cost cap exceptions. RAG solves this by grounding the model in the actual source documents — the exact use case it was designed for.

## Note

This is in progress public version, the site hosted is based on the private repository. This is so you can download it yourself, follow the future quickstart, and import your own keys.
 
## How it works
 
1. **Ingest** — FIA regulation PDFs are parsed and split into overlapping text chunks
2. **Embed** — Each chunk is converted to a vector embedding capturing its semantic meaning
3. **Store** — Vectors are indexed in ChromaDB for fast similarity search
4. **Retrieve** — User queries are embedded and matched against stored chunks using cosine similarity
5. **Generate** — The top-k relevant chunks are injected into a prompt template, and the LLM generates a grounded answer with source references
## Tech stack
 
- **Python** — core application logic
- **ChromaDB** — local vector database for embedding storage and similarity search
- **Claude API** — LLM for answer generation
- **Django** — web interface with chat UI
- **PyMuPDF** — PDF text extraction
## Project structure
 
```
f1-rag/
├── data/regulations/       # FIA regulation PDFs
├── src/
│   ├── ingest.py           # PDF → text extraction pipeline
│   ├── chunker.py          # text splitting with configurable size/overlap
│   ├── embedder.py         # embedding API calls
│   ├── retriever.py        # ChromaDB similarity search
│   ├── generator.py        # prompt construction + LLM API calls
│   └── chat.py             # CLI chat interface
├── web/                    # Django app (chat UI)
├── .env.example
├── requirements.txt
└── README.md
```
 
