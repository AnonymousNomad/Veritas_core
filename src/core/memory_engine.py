import os

class MemoryEngine:
    def ingest_knowledge(self, directory):
        # Anchor the path to the current working directory
        base_path = os.path.join(os.getcwd(), directory)
        
        if not os.path.exists(base_path):
            print(f"CRITICAL: Path {base_path} not found. Creating directory...")
            os.makedirs(base_path, exist_ok=True)
            return

        for filename in os.listdir(base_path):
            print(f"Ingesting: {filename}")
            # Your existing ingestion logic here...
