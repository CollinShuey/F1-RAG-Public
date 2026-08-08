import chromadb


client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_collection("f1_regulations")

def retrieve(query:str, k:int=5) -> list[dict]:
    r = col.query(query_texts=[query],n_results=k)
    output = []
    for meta, doc in zip(r['metadatas'][0], r['documents'][0]):
        output.append({"metadata":meta,"document":doc})
    return output


# print(retrieve("What is the minimum weight of an F1 car?",3))