import os
import json
import time
import torch
import sys

# Ensure module pathing is absolute for the internal wrapper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.transformer_wrapper import SovereignTransformer

class MemoryEngine:
    def __init__(self):
        self.embedder = SovereignTransformer(model_name="facebook/opt-125m")
        self.dim = self.embedder.dim

    def ingest_knowledge(self, directory="storage/knowledge"):
        os.makedirs(directory, exist_ok=True)
        
        try:
            files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        except OSError as e:
            print(f"[-] Critical I/O Exception: {str(e)}")
            return

        if not files:
            manifest_path = os.path.join(directory, "chunks_manifest.json")
            if not os.path.exists(manifest_path):
                with open(manifest_path, 'w') as f:
                    json.dump([], f)
            return

        print(f"[*] Processing {len(files)} source telemetry matrices via generative backbone...")
        
        all_chunks = []
        for filename in files:
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for idx, line in enumerate(lines):
                    clean_line = line.strip()
                    if clean_line:
                        all_chunks.append({
                            "chunk_id": f"txt_{filename}_L{idx+1}",
                            "source_path": filename,
                            "text": clean_line,
                            "metadata": {"start_line": idx+1, "end_line": idx+1, "type": "plain"},
                            "timestamp": time.time()
                        })
            except Exception as e:
                print(f"[!] Bypassing corrupted node {filename}: {str(e)}")

        if not all_chunks:
            return

        print(f"[*] Generating {self.dim}-dimensional tensors for localized mapping...")
        embeddings_list = []
        for chunk in all_chunks:
            embeddings_list.append(self.embedder.encode(chunk['text']))
            
        embeddings = torch.stack(embeddings_list)

        torch.save(embeddings, os.path.join(directory, "vectors_cache.pt"))
        with open(os.path.join(directory, "chunks_manifest.json"), 'w') as f:
            json.dump(all_chunks, f, indent=2)
            
        print(f"[+] Tier 1 Sovereign Matrix Compiled. {len(all_chunks)} nodes secured.")
