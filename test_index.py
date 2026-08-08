"""Throwaway sanity check for the indexing stage.

Run AFTER `python ingest.py` has populated ./chroma_db.
This does NOT re-index — it just reads the existing collection.

    python test_index.py
"""

import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_collection("f1_regulations")

# --- Test 1: did indexing store anything? ---
print("=" * 60)
print("TEST 1 — collection contents")
print("=" * 60)
count = col.count()
print(f"Total chunks stored: {count}")
if count == 0:
    print("EMPTY — run `python ingest.py` first.")
    raise SystemExit
peek = col.peek(1)  # show one stored chunk so you can eyeball the text
print(f"Sample source : {peek['metadatas'][0]['source']}")
print(f"Sample chunk  : {peek['documents'][0][:200]!r}")

# --- Test 2: is the stored data actually searchable? ---
print("\n" + "=" * 60)
print("TEST 2 — retrieval quality")
print("=" * 60)
questions = [
    "What is the minimum weight of an F1 car?",
    "How does the cost cap work?",
    "What are the tyre regulations?",
]
for q in questions:
    print(f"\nQ: {q}")
    res = col.query(query_texts=[q], n_results=3)
    for meta, doc in zip(res["metadatas"][0], res["documents"][0]):
        snippet = doc[:180].replace("\n", " ")
        print(f"  [{meta['source']}] {snippet}")
