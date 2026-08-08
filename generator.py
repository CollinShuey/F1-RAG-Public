import os
import json, re
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_llm(prompt:str) -> str:
    try:
        res = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return res.content[0].text
    except Exception as e:
        return f"LLM Error: {e}"


def break_down(query:str) -> str:
    prompt = f"""Break this into 1-3 standalone search queries that preserve the meaning of
    the original question. If it's already simple, return it unchanged. Replay as a JSON list.
    Question: {query}
    """
    res = call_llm(prompt)
    
    try:
        match = re.search(r"\[.*\]", res, re.DOTALL)
        return json.loads(match.group(0)) if match else [query]
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return [query]

def generate_answer(query:str,context:list[dict]) -> dict:
    if not context:
        return {"answer":"I couldn't find anything relevant in the regulations.","sources":[]}
    context_text = "\n\n---\n\n".join(d['document'] for d in context)
    prompt = f"""You are an F1 regulations expert. Answer only from the context provided.
    If the context does not contain the answer, say so.

    Context:
    {context_text}

    Question:
    {query}

    Answer:
    """

    res = call_llm(prompt)
    
    sources = [d["metadata"] for d in context]

    return {"answer":res,"sources":sources}
