import os
import json
import csv
import time
from dataclasses import dataclass, asdict

@dataclass
class KnowledgeChunk:
    chunk_id: str
    source_path: str
    text: str
    timestamp: float
    metadata: dict

class MemoryEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.embedder = SentenceTransformer(model_name)
        self.max_seq_length = self.embedder.get_max_seq_length() or 256
        self.chunks_manifest = []
        self.embeddings_cache = None
        self.plugins = {}
        self._load_plugins()

    def _load_plugins(self):
        """Discovers and registers custom reasoning operators dynamically from the plugins vector."""
        plugins_dir = os.path.join(os.getcwd(), "plugins")
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir, exist_ok=True)
            return
            
        # Hardcoded core system fallback operators
        self.plugins["SUPPORTS"] = lambda a, b: float(torch.cosine_similarity(a, b, dim=0))
        self.plugins["CONTRADICTS"] = lambda a, b: float(1.0 - torch.cosine_similarity(a, b, dim=0))

    def ingest_knowledge(self, directory):
        """Scans directory, executes structure-first parsing, stamps temporal tracking data, and vectorizes."""
        base_path = os.path.join(os.getcwd(), directory)
        if not os.path.exists(base_path):
            print(f"CRITICAL: Path {base_path} not found. Creating directory...")
            os.makedirs(base_path, exist_ok=True)
            return

        all_chunks = []
        execution_time = time.time()  # Unified temporal anchor for this ingestion sequence

        for root, _, files in os.walk(base_path):
            for filename in files:
                # Filter out system tracking manifests
                if filename in ["chunks_manifest.json", "vectors_cache.pt"]:
                    continue
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, base_path)
                
                if filename.endswith(('.txt', '.md', '.rst')):
                    chunks = self._parse_txt(file_path, rel_path, execution_time)
                elif filename.endswith(('.json', '.jsonl')):
                    chunks = self._parse_json(file_path, rel_path, execution_time)
                elif filename.endswith(('.csv', '.tsv')):
                    chunks = self._parse_csv(file_path, rel_path, execution_time)
                else:
                    chunks = self._parse_fallback(file_path, rel_path, execution_time)
                
                if chunks:
                    all_chunks.extend(chunks)

        if not all_chunks:
            return

        self._generate_embeddings(all_chunks)
        self._save_manifest(base_path)

    def _parse_txt(self, file_path, rel_path, timestamp):
        chunks = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            buffer, buffer_chars, start_line = [], 0, 1
            for idx, line in enumerate(lines, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                buffer.append(clean_line)
                buffer_chars += len(clean_line)
                if buffer_chars >= 1000:
                    chunks.append(KnowledgeChunk(
                        chunk_id=f"txt_{rel_path.replace('/', '_')}_L{start_line}",
                        source_path=rel_path,
                        text=" ".join(buffer),
                        timestamp=timestamp,
                        metadata={"type": "plain", "start_line": start_line, "end_line": idx}
                    ))
                    buffer, buffer_chars, start_line = [], 0, idx + 1
            if buffer:
                chunks.append(KnowledgeChunk(
                    chunk_id=f"txt_{rel_path.replace('/', '_')}_L{start_line}",
                    source_path=rel_path,
                    text=" ".join(buffer),
                    timestamp=timestamp,
                    metadata={"type": "plain", "start_line": start_line, "end_line": len(lines)}
                ))
        except Exception as e:
            print(f"[!] Processing error: {str(e)}")
        return chunks

    def _parse_json(self, file_path, rel_path, timestamp):
        chunks = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                if file_path.endswith('.jsonl'):
                    records = [json.loads(line) for line in f if line.strip()]
                else:
                    data = json.load(f)
                    records = data if isinstance(data, list) else [data]
            for idx, record in enumerate(records):
                for k, v in record.items():
                    if isinstance(v, str) and len(v) >= 20:
                        chunks.append(KnowledgeChunk(
                            chunk_id=f"json_{rel_path.replace('/', '_')}_R{idx}_{k}",
                            source_path=rel_path,
                            text=v,
                            timestamp=timestamp,
                            metadata={"type": "json", "record_index": idx, "key_path": k}
                        ))
        except Exception:
            return self._parse_fallback(file_path, rel_path, timestamp)
        return chunks

    def _parse_csv(self, file_path, rel_path, timestamp):
        chunks = []
        try:
            delimiter = '\t' if file_path.endswith('.tsv') else ','
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                for idx, row in enumerate(reader, start=1):
                    text_parts, meta_fields = [], {}
                    for k, v in row.items():
                        if not k or not v: continue
                        if len(v) > 30 or any(x in k.lower() for x in ['desc', 'note', 'text', 'body', 'message']):
                            text_parts.append(f"{k}: {v}")
                        else:
                            meta_fields[k] = v
                    if text_parts:
                        meta_fields.update({"type": "csv", "row_index": idx})
                        chunks.append(KnowledgeChunk(
                            chunk_id=f"csv_{rel_path.replace('/', '_')}_R{idx}",
                            source_path=rel_path,
                            text=" | ".join(text_parts),
                            timestamp=timestamp,
                            metadata=meta_fields
                        ))
        except Exception:
            return self._parse_fallback(file_path, rel_path, timestamp)
        return chunks

    def _parse_fallback(self, file_path, rel_path, timestamp):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(10000).strip()
            if len(content) > 50:
                return [KnowledgeChunk(
                    chunk_id=f"fallback_{rel_path.replace('/', '_')}",
                    source_path=rel_path,
                    text=content,
                    timestamp=timestamp,
                    metadata={"type": "fallback_stream"}
                )]
        except Exception:
            pass
        return []

    def _generate_embeddings(self, chunks):
        import torch
        texts = [c.text for c in chunks]
        batch_size = 32
        embeddings_list = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_embeds = self.embedder.encode(batch_texts, convert_to_tensor=True, show_progress_bar=False)
            embeddings_list.append(batch_embeds.cpu())
        self.embeddings_cache = torch.cat(embeddings_list, dim=0)
        self.chunks_manifest = [asdict(c) for c in chunks]

    def _save_manifest(self, base_path):
        import torch
        with open(os.path.join(base_path, "chunks_manifest.json"), 'w', encoding='utf-8') as f:
            json.dump(self.chunks_manifest, f, indent=4)
        if self.embeddings_cache is not None:
            torch.save(self.embeddings_cache, os.path.join(base_path, "vectors_cache.pt"))

if __name__ == "__main__":
    engine = MemoryEngine()
    engine.ingest_knowledge('storage/knowledge')
