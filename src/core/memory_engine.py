from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

class MemoryEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []

    def ingest_knowledge(self, directory):
        for filename in os.listdir(directory):
            with open(os.path.join(directory, filename), 'r') as f:
                content = f.read()
                self.documents.append(content)
        embeddings = self.model.encode(self.documents)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))

    def query(self, user_input):
        query_vector = self.model.encode([user_input])
        D, I = self.index.search(np.array(query_vector).astype('float32'), k=1)
        return self.documents[I[0][0]]
