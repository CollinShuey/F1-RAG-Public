"""
LangChain version of the F1 Regulations RAG pipeline — a side-by-side reference.

NOT used by the deployed site. Production runs the from-scratch pipeline
(ingest / embedder / retriever / generator / agent). This file rebuilds the
*base* RAG flow with LangChain to compare hand-rolled vs. framework code.

Kept identical for a fair comparison:
  - the same structure-aware chunker (chunk_by_structure from chunker.py)
  - the same embedding model (all-MiniLM-L6-v2)
LangChain only takes over: embed -> store -> retrieve -> prompt -> generate.

Setup + run:
    pip install langchain langchain-classic langchain-anthropic langchain-chroma langchain-huggingface sentence-transformers
    python langchain_pipeline.py ingest     # build the vector store once
    python langchain_pipeline.py            # ask questions
"""

import sys
from pathlib import Path

import fitz
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from chunker import chunk_by_structure  # reuse the exact same custom chunker

load_dotenv()

REG_DIR = Path("data/regulations")
DB_DIR = "./chroma_langchain_db"   # separate dir so it never touches production chroma_db
COLLECTION = "f1_regulations_lc"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def ingest():
    """PDFs -> chunks -> Chroma. Replaces ingest.py + embedder.py."""
    docs = []
    for pdf_path in REG_DIR.glob("*.pdf"):
        pdf = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in pdf)
        pdf.close()
        for c in chunk_by_structure(text):        # same custom chunker
            docs.append(Document(
                page_content=c["text"],
                metadata={"source": pdf_path.name, "section": c["section"]},
            ))
    Chroma.from_documents(docs, embeddings, persist_directory=DB_DIR, collection_name=COLLECTION)
    print(f"Embedded {len(docs)} chunks into {DB_DIR}")


def build_chain():
    """Replaces retriever.py + generator.py (query, prompt, API call, parsing)."""
    vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_template(
        "You are an F1 regulations expert. Answer only from the context provided. "
        "If the context does not contain the answer, say so.\n\n"
        "Context:\n{context}\n\nQuestion: {input}\n\nAnswer:"
    )
    llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=1024)

    # stuff_documents formats retrieved docs into {context}; retrieval_chain wires
    # the retriever to it and returns {"answer", "context"}.
    doc_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, doc_chain)


def ask(chain, question: str) -> dict:
    result = chain.invoke({"input": question})
    sources = sorted({d.metadata.get("section") for d in result["context"]})
    return {"answer": result["answer"], "sources": sources}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ingest":
        ingest()
        sys.exit()

    if not Path(DB_DIR).exists():
        sys.exit(f"No vector store at {DB_DIR}. Run:  python langchain_pipeline.py ingest")
    # build langchain chain, replaces the retriever.py and generator.py, every ask invokes
    # this chain and passes in the question, the context gets automatically filled in when invoked
    chain = build_chain()   # built once, reused for every question
    print("F1 Regulations Bot (LangChain version). Type 'quit' to exit.")
    while True:
        q = input("\nAsk: ").strip()
        if q.lower() in ("quit", "exit"):
            break
        if not q:
            continue
        res = ask(chain, q)
        print("\n" + res["answer"])
        print("\nSources:", ", ".join(s for s in res["sources"] if s))



