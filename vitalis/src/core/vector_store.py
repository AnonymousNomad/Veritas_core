import json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from ...logger import logger
from ...config import load_config

_cfg = load_config()
STORAGE = Path(_cfg["storage_root"]) / "storage"
INDEX_DIR = STORAGE / "faiss_index"
KNOWLEDGE_DIR = STORAGE / "knowledge"

class VectorStore:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.doc_texts = []
        self._load_or_build()

    def _load_or_build(self):
        if INDEX_DIR.is_dir() and (INDEX_DIR / "index.faiss").exists():
            logger.info("Loading existing local FAISS index")
            self.index = faiss.read_index(str(INDEX_DIR / "index.faiss"))
            with (INDEX_DIR / "metadata.json").open("r", encoding="utf-8") as f:
                self.doc_texts = json.load(f)["texts"]
        else:
            self._build_index()

    def _build_index(self):
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        docs = [p.read_text(encoding="utf-8") for p in KNOWLEDGE_DIR.rglob("*") if p.suffix in {".txt", ".md"}]
        if not docs:
            logger.warning(f"No knowledge files found in {KNOWLEDGE_DIR}.")
            self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
            return
        embeddings = self.model.encode(docs, normalize_embeddings=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings, dtype="float32"))
        self.doc_texts = docs
        faiss.write_index(self.index, str(INDEX_DIR / "index.faiss"))
        with (INDEX_DIR / "metadata.json").open("w", encoding="utf-8") as f:
            json.dump({"texts": self.doc_texts}, f)

    def search(self, query: str, top_k: int = 3):
        if self.index is None or self.index.ntotal == 0: return []
        q_vec = self.model.encode([query], normalize_embeddings=True)
        _, I = self.index.search(np.array(q_vec, dtype="float32"), top_k)
        return [self.doc_texts[idx] for idx in I[0] if 0 <= idx < len(self.doc_texts)]
