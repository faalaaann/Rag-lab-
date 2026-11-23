import os
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types

load_dotenv()

# --- CONFIGURATION (Toggle CHUNK_SIZE between 200 and 1000 for Task 4) ---
WORKSPACE = Path(__file__).resolve().parent
PDF_CANDIDATES = [
    WORKSPACE / "cloudops m3.pdf",
    Path.home() / "Downloads" / "cloudops m3.pdf",
]
PDF_PATH = next(
    (str(path) for path in PDF_CANDIDATES if path.is_file() and path.stat().st_size > 0),
    None,
)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "80"))

# 1. LOAD & CHUNK
if PDF_PATH is None:
    raise FileNotFoundError(
        "PDF not found. Place 'cloudops m3.pdf' in the project folder "
        "or in your Downloads folder."
    )

pdf_path = Path(PDF_PATH)
if not pdf_path.is_file():
    raise FileNotFoundError(f"PDF not found: {pdf_path}")

reader = PdfReader(pdf_path)
raw_text = "\n".join(page.extract_text() or "" for page in reader.pages)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
chunks = splitter.split_text(raw_text)
print(f"[Chunk Size: {CHUNK_SIZE}] Extracted {len(chunks)} chunks from {PDF_PATH}")

# 2. EMBED & STORE IN MEMORY (Normalized vectors for fast cosine similarity)
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chunk_embeddings = embedder.encode(chunks, normalize_embeddings=True)
print("Indexed all chunks in memory.\n")

# 3. RETRIEVE TOP-K CHUNKS
def retrieve(query, k=3):
    query_vec = embedder.encode([query], normalize_embeddings=True)[0]
    similarities = np.dot(chunk_embeddings, query_vec)
    top_indices = np.argsort(similarities)[::-1][:k]
    return [chunks[i] for i in top_indices]

# 4. GENERATE GROUNDED ANSWER WITH GEMINI
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def ask_pdf(question):
    top_chunks = retrieve(question, k=3)
    context = "\n\n---\n\n".join(top_chunks)

    prompt = f"""Answer using ONLY the context below.
If the answer isn't in the context, say so.

Context:
{context}

Question: {question}"""

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )
    print(f"Q: {question}")
    print(f"A: {response.text}")
    print("-" * 60)


if __name__ == "__main__":
    print("Ask a question about the PDF (type 'exit' to quit).")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if question:
            ask_pdf(question)