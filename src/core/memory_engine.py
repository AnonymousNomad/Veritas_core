class MemoryEngine:
    def __init__(self):
        print("Initializing MemoryEngine...")
        import faiss
        self.faiss = faiss
        print("FAISS loaded successfully.")
