from generator import break_down
from retriever import retrieve
from generator import generate_answer

def agent_query(query: str,k:int=5) -> dict:
    sub_queries = break_down(query) # This is the 1-3 searches to decompose the query, giving llm richer context
    print("sub-queries:", sub_queries)
    all_chunks = []
    for sq in sub_queries:
        all_chunks.extend(retrieve(sq,k=k))

    seen,unique = set(),[]
    for c in all_chunks:
        if c["document"] not in seen:
            unique.append(c)
            seen.add(c["document"])
    res = generate_answer(query,unique)
    res["chunks"] = unique
    return res

    