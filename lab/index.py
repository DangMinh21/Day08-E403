"""
index.py — Sprint 1: Build RAG Index
====================================
Mục tiêu Sprint 1 (60 phút):
  - Đọc và preprocess tài liệu từ data/docs/
  - Chunk tài liệu theo cấu trúc tự nhiên (heading/section)
  - Gắn metadata: source, section, department, effective_date, access
  - Embed và lưu vào vector store (ChromaDB)

Definition of Done Sprint 1:
  ✓ Script chạy được và index đủ docs
  ✓ Có ít nhất 3 metadata fields hữu ích cho retrieval
  ✓ Có thể kiểm tra chunk bằng list_chunks()
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CẤU HÌNH
# =============================================================================

DOCS_DIR = Path(__file__).parent / "data" / "docs"
CHROMA_DB_DIR = Path(__file__).parent / "chroma_db"

# TODO Sprint 1: Điều chỉnh chunk size và overlap theo quyết định của nhóm
# Gợi ý từ slide: chunk 300-500 tokens, overlap 50-80 tokens
CHUNK_SIZE = 400       # tokens (ước lượng bằng số ký tự / 4)
CHUNK_OVERLAP = 80     # tokens overlap giữa các chunk

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
LOCAL_EMBEDDING_MODEL = os.getenv(
    "LOCAL_EMBEDDING_MODEL",
    "paraphrase-multilingual-MiniLM-L12-v2",
)

_OPENAI_CLIENT = None
_LOCAL_EMBED_MODEL = None


# =============================================================================
# STEP 1: PREPROCESS
# Làm sạch text trước khi chunk và embed
# =============================================================================

def preprocess_document(raw_text: str, filepath: str) -> Dict[str, Any]:
    """
    Preprocess a document: extract metadata from the header and clean the content.
    """
    lines = raw_text.strip().split("\n")
    metadata = {
        "source": filepath,
        "section": "",
        "department": "unknown",
        "effective_date": "unknown",
        "access": "internal",
    }
    content_lines = []
    header_done = False

    for line in lines:
        if not header_done:
            if line.startswith("Source:"):
                metadata["source"] = line.replace("Source:", "").strip()
            elif line.startswith("Department:"):
                metadata["department"] = line.replace("Department:", "").strip()
            elif line.startswith("Effective Date:"):
                metadata["effective_date"] = line.replace("Effective Date:", "").strip()
            elif line.startswith("Access:"):
                metadata["access"] = line.replace("Access:", "").strip()
            elif line.startswith("==="):
                header_done = True
                content_lines.append(line)
            elif line.strip() == "" or line.isupper():
                continue
        else:
            content_lines.append(line)

    cleaned_text = "\n".join(content_lines)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    return {
        "text": cleaned_text,
        "metadata": metadata,
    }


# =============================================================================
# STEP 2: CHUNK
# Chia tài liệu thành các đoạn nhỏ theo cấu trúc tự nhiên
# =============================================================================

def chunk_document(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Split text into chunks of specified size with overlap.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


# =============================================================================
# STEP 3: EMBED + STORE
# Embed các chunk và lưu vào ChromaDB
# =============================================================================

def get_embedding(text: str) -> List[float]:
    """
    Tạo embedding vector cho một đoạn text.

    TODO Sprint 1:
    Chọn một trong hai:

    Option A — OpenAI Embeddings (cần OPENAI_API_KEY):
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    Option B — Sentence Transformers (chạy local, không cần API key):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        return model.encode(text).tolist()
    """
    global _OPENAI_CLIENT, _LOCAL_EMBED_MODEL

    clean_text = " ".join(text.split())
    if not clean_text:
        clean_text = "."

    if EMBEDDING_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Thiếu OPENAI_API_KEY. "
                "Hãy thêm key vào .env hoặc đặt EMBEDDING_PROVIDER=local."
            )
        if _OPENAI_CLIENT is None:
            from openai import OpenAI
            _OPENAI_CLIENT = OpenAI(api_key=api_key)

        response = _OPENAI_CLIENT.embeddings.create(
            input=clean_text,
            model=OPENAI_EMBEDDING_MODEL,
        )
        return response.data[0].embedding

    if EMBEDDING_PROVIDER == "local":
        if _LOCAL_EMBED_MODEL is None:
            from sentence_transformers import SentenceTransformer
            _LOCAL_EMBED_MODEL = SentenceTransformer(LOCAL_EMBEDDING_MODEL)
        return _LOCAL_EMBED_MODEL.encode(clean_text).tolist()

    raise ValueError(
        f"EMBEDDING_PROVIDER không hợp lệ: {EMBEDDING_PROVIDER}. "
        "Dùng 'openai' hoặc 'local'."
    )


def build_index():
    """
    Build the document index and store it in ChromaDB.
    """
    from chromadb import PersistentClient

    client = PersistentClient(path=str(CHROMA_DB_DIR))
    collection = client.get_or_create_collection("rag_lab")

    for doc_path in DOCS_DIR.glob("*.txt"):
        with open(doc_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        processed = preprocess_document(raw_text, str(doc_path))
        chunks = chunk_document(processed["text"], CHUNK_SIZE, CHUNK_OVERLAP)

        for chunk in chunks:
            collection.upsert(
                documents=[chunk],
                metadatas=[processed["metadata"]]
            )

if __name__ == "__main__":
    build_index()
