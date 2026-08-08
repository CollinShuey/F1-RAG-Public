import fitz
from chunker import chunk_by_structure

doc = fitz.open("data/regulations/FIA 2026 F1 Regulations - Section C [Technical] - Iss 19 - 2026-06-25.pdf")
text = "\n".join(p.get_text() for p in doc[3:])
for c in chunk_by_structure(text)[:40]:
    print(c["section"], "→", c["text"][:60].replace("\n", " "))
