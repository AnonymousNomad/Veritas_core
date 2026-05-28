import os
import json
import csv
import math
from dataclasses import dataclass, asdict

@dataclass
class KnowledgeChunk:
    chunk_id: str
    source_path: str
    text: str
    metadata: dict

class MemoryEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Lazy import of heavy ML libraries to keep initial startup fast
        from sentence_transformers import SentenceTransformer
        self.embedder = SentenceTransformer(model_name)
        self.max_seq_length = self.embedder.get_max_seq_length() or 256
        self.chunks_manifest = []
        self.embeddings_cache = None

    def ingest_knowledge(self, directory):
        """Scans directory, parses supported files, generates semantic chunks, and vectorizes them."""
        base_path = os.path.join(os.getcwd(), directory)
        
        if not os.path.exists(base_path):
            print(f"CRITICAL: Path {base_path} not found. Creating directory...")
            os.makedirs(base_path, exist_ok=True)
            return

        all_chunks = []
        print(f"[*] Beginning execution sweep over data matrix: {base_path}")

        for root, _, files in os.walk(base_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, base_path)
                
                # Format Dispatcher Matrix
                if filename.endswith(('.txt', '.md', '.rst')):
                    chunks = self._parse_txt(file_path, rel_path)
                elif filename.endswith(('.json', '.jsonl')):
                    chunks = self._parse_json(file_path, rel_path)
                elif filename.endswith(('.csv', '.tsv')):
                    chunks = self._parse_csv(file_path, rel_path)
                else:
                    chunks = self._parse_fallback(file_path, rel_path)
                
                if chunks:
                    all_chunks.extend(chunks)
                    print(f"[+] Extracted {len(chunks)} chunks from: {rel_path}")

        if not all_chunks:
            print("[!] Operation complete: No valid text blocks extracted for vectorization.")
            return

        self._generate_embeddings(all_chunks)
        self._save_manifest(base_path)

    def _parse_txt(self, file_path, rel_path):
        chunks = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Group rows sequentially into basic paragraph-sized contextual windows
            buffer = []
            buffer_chars = 0
            start_line = 1
            
            for idx, line in enumerate(lines, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                buffer.append(clean_line)
                buffer_chars += len(clean_line)
                
                if buffer_chars >= 1000:  # ~200-250 words architectural chunk threshold
                    text_content = " ".join(buffer)
                    chunk_id = f"txt_{rel_path.replace('/', '_')}_L{start_line}"
                    chunks.append(KnowledgeChunk(
                        chunk_id=chunk_id,
                        source_path=rel_path,
                        text=text_content,
                        metadata={"type": "plain", "start_line": start_line, "end_line": idx}
                    ))
                    buffer = []
                    buffer_chars = 0
                    start_line = idx + 1
                    
            if buffer:  # Clean up remaining trailing lines
                text_content = " ".join(buffer)
                chunks.append(KnowledgeChunk(
                    chunk_id=f"txt_{rel_path.replace('/', '_')}_L{start_line}",
                    source_path=rel_path,
                    text=text_content,
                    metadata={"type": "plain", "start_line": start_line, "end_line": len(lines)}
                ))
        except Exception as e:
            print(f"[!] Error processing text file {rel_path}: {str(e)}")
        return chunks

    def _parse_json(self, file_path, rel_path):
        chunks = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                if file_path.endswith('.jsonl'):
                    records = [json.loads(line) for line in f if line.strip()]
                else:
                    data = json.load(f)
                    records = data if isinstance(data, list) else [data]
            
            for idx, record in enumerate(records):
                # Isolate string values matching natural language heuristic properties
                for key, val in record.items():
                    if isinstance(val, str) and len(val) >= 20:
                        chunk_id = f"json_{rel_path.replace('/', '_')}_R{idx}_{key}"
                        chunks.append(KnowledgeChunk(
                            chunk_id=chunk_id,
                            source_path=rel_path,
                            text=val,
                            metadata={"type": "json", "record_index": idx, "key_path": key}
                        ))
        except Exception as e:
            print(f"[!] Error processing structured JSON {rel_path}: {str(e)}")
            return self._parse_fallback(file_path, rel_path)
        return chunks

    def _parse_csv(self, file_path, rel_path):
        chunks = []
        try:
            delimiter = '\t' if file_path.endswith('.tsv') else ','
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                for idx, row in enumerate(reader, start=1):
                    # Combine dense text cells while keeping numeric structural attributes tied as metadata
                    text_parts = []
                    meta_fields = {}
                    for k, v in row.items():
                        if not k or not v:
                            continue
                        # Heuristic check for natural language strings vs identifiers/counters
                        if len(v) > 30 or any(x in k.lower() for x in ['desc', 'note', 'text', 'body', 'message', 'data']):
                            text_parts.append(f"{k}: {v}")
                        else:
                            meta_fields[k] = v
                    
                    if text_parts:
                        combined_text = " | ".join(text_parts)
                        chunk_id = f"csv_{rel_path.replace('/', '_')}_R{idx}"
                        meta_fields.update({"type": "csv", "row_index": idx})
                        chunks.append(KnowledgeChunk(
                            chunk_id=chunk_id,
                            source_path=rel_path,
                            text=combined_text,
                            metadata=meta_fields
                        ))
        except Exception as e:
            print(f"[!] Error processing spreadsheet matrix {rel_path}: {str(e)}")
            return self._parse_fallback(file_path, rel_path)
        return chunks

    def _parse_fallback(self, file_path, rel_path):
        """Emergency safe-mode logic path to pull text securely from unidentified binary fragments."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(10000).strip() # Extract first 10k characters safely
            if len(content) > 50:
                return [KnowledgeChunk(
                    chunk_id=f"fallback_{rel_path.replace('/', '_')}",
                    source_path=rel_path,
                    text=content,
                    metadata={"type": "fallback_stream"}
                )]
        except Exception:
            pass
        return []

    def _generate_embeddings(self, chunks):
        """Batches and vectorizes parsed objects with the active Transformer context matrix."""
        import torch
        print(f"[*] Encoding {len(chunks)} text chunks into unified coordinate vector space...")
        
        texts = [c.text for c in chunks]
        
        # Execution execution batch slice for low-overhead ARM64 memory profiles
        batch_size = 32
        embeddings_list = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            # Convert text streams into normalized vector spaces
            batch_embeds = self.embedder.encode(batch_texts, convert_to_tensor=True, show_progress_bar=False)
            embeddings_list.append(batch_embeds.cpu())
            
        self.embeddings_cache = torch.cat(embeddings_list, dim=0)
        self.chunks_manifest = [asdict(c) for c in chunks]
        print(f"[+] Multi-dimensional vector calculation sequence resolved: {self.embeddings_cache.shape}")

    def _save_manifest(self, base_path):
        """Serializes the engine metadata matrix and tensor index to local scratch storage."""
        import torch
        manifest_path = os.path.join(base_path, "chunks_manifest.json")
        vectors_path = os.path.join(base_path, "vectors_cache.pt")
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.chunks_manifest, f, indent=4)
            
        if self.embeddings_cache is not None:
            torch.save(self.embeddings_cache, vectors_path)
            
        print(f"[+] Storage sync finalized. Manifest recorded at: {manifest_path}")
        print(f"[+] Vector tensor cache secured at: {vectors_path}")

if __name__ == "__main__":
    # Internal execution harness verification loop
    engine = MemoryEngine()
    engine.ingest_knowledge('storage/knowledge')
