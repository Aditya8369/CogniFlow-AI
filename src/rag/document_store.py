import os
import chromadb
from pypdf import PdfReader
from src.core.config import config

class DocumentStore:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=config.chroma_db_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="course_materials")

    def ingest_pdf(self, file_path: str, doc_id: str):
        reader = PdfReader(file_path)
        chunks = []
        ids = []
        metadatas = []

        chunk_size = 500
        stride = 100

        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + " "

        words = full_text.split()
        for i in range(0, len(words), chunk_size - stride):
            chunk = " ".join(words[i : i + chunk_size])
            if chunk.strip():
                cid = f"{doc_id}_chunk_{i}"
                chunks.append(chunk)
                ids.append(cid)
                metadatas.append({"doc_id": doc_id, "index": i})

        if chunks:
            self.collection.add(
                documents=chunks,
                ids=ids,
                metadatas=metadatas
            )

    def retrieve_context(self, query: str, n_results: int = 3) -> str:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        docs = results.get("documents", [[]])[0]
        return "\n\n".join(docs) if docs else ""