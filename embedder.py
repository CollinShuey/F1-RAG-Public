import chromadb


def embedder(chunks,all_sources,all_sections):
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("f1_regulations")
    except:
        pass
    collection = client.get_or_create_collection("f1_regulations")
    collection.add(
        documents= chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": source, "section": section} for source, section in zip(all_sources, all_sections)]
    )
    print(f"Embedded {collection.count()} chunks.")
    