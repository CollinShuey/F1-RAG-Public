import re

header_pattern = re.compile(r"^([ABCDE]\d+(?:\.\d+)*)\s")

def chunk_by_structure(text: str, max_chars: int = 1500) -> list[dict]:
    lines = text.split("\n")
    chunks = []
    buffer =[]
    current = "preamble"

    def flush():
        body = "\n".join(buffer).strip()
        if len(body) < 50:
            return
        if not body:
            return
        if len(body) > max_chars:
            for i in range(0,len(body), max_chars - 200):
                chunks.append({"section": current, "text": body[i:i+max_chars]})
            return
        chunks.append({"section": current, "text": body})
    for line in lines:
        m = header_pattern.match(line)
        if m:
            flush()
            current = m.group(1)
            buffer = [line]
        else:
            buffer.append(line)
    flush()
    return chunks


def chunk_text(text: str, chunk_size: int = 500,overlap:int=100) -> list[str]:
    chunks = []
    s = 0
    while s < len(text):
        chunks.append(text[s:s+chunk_size])
        s += chunk_size-overlap
    return chunks