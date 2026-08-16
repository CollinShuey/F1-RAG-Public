# F1 Regs AI
 
An AI-powered chatbot that answers questions about FIA Formula 1 regulations using Retrieval-Augmented Generation (RAG). Built from scratch with Python and ChromaDB, no frameworks, to deeply understand the RAG pipeline, then refactored with LangChain for comparison.
 
> **Why F1 regulations?** LLMs can't reliably answer detailed questions about specific regulation clauses, minimum car weights, or cost cap exceptions. RAG solves this by grounding the model in the actual source documents, the exact use case it was designed for.

## Note

This is in progress public version, the site hosted is based on the private repository. This is so you can download it yourself, follow the quickstart below, and import your own keys.

The hosted site can found [here](https://formula1-rag.onrender.com).
 
## How it works
 
1. **Ingest**: FIA regulation PDFs are parsed and split into overlapping text chunks
2. **Embed**: Each chunk is converted to a vector embedding capturing its semantic meaning
3. **Store**: Vectors are indexed in ChromaDB for fast similarity search
4. **Retrieve**: User queries are embedded and matched against stored chunks using cosine similarity
5. **Generate**: The top-k relevant chunks are injected into a prompt template, and the LLM generates a grounded answer with source references
## Tech stack
 
- **Python**: core application logic
- **ChromaDB**: local vector database for embedding storage and similarity search
- **Claude API**: LLM for answer generation
- **Django**: web interface with chat UI
- **PyMuPDF**: PDF text extraction


## Quick start (run it locally)

### Prerequisites

- Python 3.12
- An Anthropic API key ([console.anthropic.com](https://console.anthropic.com)), used for answer generation. A few dollars of credit is plenty; questions cost fractions of a cent on Claude Haiku.
- The FIA regulation PDFs (see step 4, you download these yourself; they aren't included in this repo).

### 1. Clone and enter the project

    git clone https://github.com/CollinShuey/F1-RAG-Public.git

### 2. Create and activate a virtual environment

    python -m venv .venv

    # Windows (PowerShell)
    .venv\Scripts\Activate.ps1

    # macOS / Linux
    source .venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Add the regulation PDFs

The FIA regulations are copyrighted, so they aren't distributed here, download them yourself (they're free public PDFs) from the FIA regulations page: https://www.fia.com/regulation/category/110

Create a `data/regulations/` folder and drop the PDFs in:

    data/regulations/
    ├── FIA F1 Technical Regulations.pdf
    ├── FIA F1 Sporting Regulations.pdf
    ├── FIA F1 General Regulations.pdf
    └── FIA F1 Financial Regulations.pdf

Any subset works, the pipeline ingests whatever PDFs are in that folder. Grab the most recent issue of each.

### 5. Add your API key

Create a `.env` file in the project root:

    ANTHROPIC_API_KEY=sk-ant-your-key-here
    DEBUG=True

`.env` is gitignored, your key never leaves your machine. `DEBUG=True` is needed for local development (production settings force HTTPS, which breaks local `runserver`).

### 6. Build the vector index

This reads the PDFs, chunks them on their article structure, embeds the chunks, and stores everything in a local ChromaDB. Run it once (re-run only when the PDFs change):

    python ingest.py

The first run downloads a small embedding model (~80 MB) and creates a `chroma_db/` folder. When it prints the number of embedded chunks, the index is built.

### 7. Ask it questions

**Command line:**

    python chat.py

Then type questions like _"What is the minimum mass of the car during qualifying?"_ or _"How is the Nominal Tyre Mass determined?"_. Add `--verbose` to also see the retrieved chunks and their sections.

**Web interface:**

    python manage.py migrate      # first time only, sets up Django's built-in tables
    python manage.py runserver

Open http://127.0.0.1:8000 and ask questions in the browser. Answers render with their cited article numbers underneath.

### (Optional) Run the evaluation

The `eval/` folder contains a test set and a harness that measures retrieval hit-rate and citation accuracy:

    python eval/run_eval.py

## LangChain comparison

A LangChain version of the F1 Regulations RAG pipeline is found in langchain_pipeline.py.

Not used by the deployed site. Production runs the from-scratch pipeline (ingest / embedder / retriever / generator / agent). This file rebuilds the base RAG flow with LangChain to compare hand-rolled vs. framework code.

Kept identical for a fair comparison:

the same structure-aware chunker (chunk_by_structure from chunker.py)
the same embedding model (all-MiniLM-L6-v2)

LangChain only takes over: embed → store → retrieve → prompt → generate.

Setup and run:

    pip install langchain langchain-classic langchain-anthropic langchain-chroma langchain-huggingface sentence-transformers

    python langchain_pipeline.py ingest

    python langchain_pipeline.py

Ingest is run to create the ChromaDB, the file is then run to ask questions.
