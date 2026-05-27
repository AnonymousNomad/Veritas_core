#!/usr/bin/env python3
import numpy as np
import re
from typing import List, Dict

class TFIDFPromptCache:
    def __init__(self):
        self.documents: List[str] = []
        self.vocab: Dict[str, int] = {}
        self.tfidf_matrix: np.ndarray = np.array([[]])

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def fit_documents(self, docs: List[str]):
        if not docs: return
        self.documents = docs
        raw_tokens = [self.tokenize(d) for d in docs]
        
        vocab_set = set()
        for tokens in raw_tokens: vocab_set.update(tokens)
        self.vocab = {word: i for i, word in enumerate(sorted(vocab_set))}
        
        N = len(docs)
        V = len(self.vocab)
        if V == 0: return
            
        tf = np.zeros((N, V))
        df = np.zeros(V)

        for i, tokens in enumerate(raw_tokens):
            for t in tokens:
                if t in self.vocab: tf[i, self.vocab[t]] += 1
            for t in set(tokens):
                if t in self.vocab: df[self.vocab[t]] += 1

        idf = np.log((1 + N) / (1 + df)) + 1
        self.tfidf_matrix = tf * idf
        norms = np.linalg.norm(self.tfidf_matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.tfidf_matrix = self.tfidf_matrix / norms

    def query(self, query_str: str, top_k: int = 2) -> List[str]:
        if self.tfidf_matrix.size == 0 or not self.vocab: return []
        tokens = self.tokenize(query_str)
        query_vec = np.zeros(len(self.vocab))
        for t in tokens:
            if t in self.vocab: query_vec[self.vocab[t]] += 1
        q_norm = np.linalg.norm(query_vec)
        if q_norm > 0: query_vec /= q_norm
        scores = np.dot(self.tfidf_matrix, query_vec)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.documents[idx] for idx in top_indices if scores[idx] > 0]
