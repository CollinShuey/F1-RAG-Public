from retriever import retrieve
from agent import agent_query
from generator import generate_answer


def chat_loop(verbose:bool=False):
    print("F1 Regulations Bot. Type 'quit' to exit.")
    while True:
        query = input("Ask: ")
        if query.strip().lower() == "quit":
            break
        if not query.strip():
            continue
        # context = retrieve(query)
        res = agent_query(query)
        if verbose:
            print("\nRetrieved Chunks:\n")
            for i,chunk in enumerate(res.get("chunks",[])):
                print(f"[{i}] section={chunk['metadata'].get('section')} source={chunk['metadata']['source']}")
                print(chunk["document"][:300], "...\n")
            print("--- end chunks ---\n")
        
        print("Answer:",res["answer"])
        print("\nSources:",res["sources"])
        print("-"*40)




if __name__ == "__main__":
    chat_loop(True)

