import json
from retriever import retrieve

def normalize(s: str) -> str:
    return " ".join(s.lower().split())   # collapse whitespace, lowercase

def run_eval(path="eval/testset_technical_section.json", k=3):
    tests = json.load(open(path))
    hits, cite_hits = 0, 0

    for t in tests:
        chunks = retrieve(t['q'], k=k)
        blob = normalize(" ".join(c["document"] for c in chunks))
        sections = {c["metadata"].get("section") for c in chunks}

        hit = normalize(t["expect_substring"]) in blob
        cite = t["expect_section"] in sections

        hits += hit
        cite_hits += cite
        print(f"{'✓' if hit else '✗'} retrieval | "
              f"{'✓' if cite else '·'} cite | {t['q'][:50]}")

    n = len(tests)
    print(f"\nRetrieval hit-rate: {hits}/{n} = {hits/n:.0%}")
    print(f"Citation accuracy:  {cite_hits}/{n} = {cite_hits/n:.0%}")

if __name__ == "__main__":
    run_eval()


        