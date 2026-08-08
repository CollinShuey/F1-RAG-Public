import fitz  # PyMuPDF
from pathlib import Path
from chunker import chunk_text, chunk_by_structure
from embedder import embedder

REG_DIR = Path("data/regulations")



all_chunks = []
all_sources =[]
all_sections = []
for pdf_path in REG_DIR.glob("*.pdf"):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc[3:])
    doc.close()
    for c in chunk_by_structure(text):
        all_chunks.append(c["text"])
        all_sections.append(c["section"])
        all_sources.append(pdf_path.name)

embedder(all_chunks,all_sources,all_sections)












    