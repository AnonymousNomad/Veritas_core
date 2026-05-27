import json
import numpy as np
from pathlib import Path
from ...logger import logger

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))

class TinyGatedRNN:
    def __init__(self, vocab_size=4000, embed_dim=128, hidden_dim=256):
        np.random.seed(42)
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self.E = np.random.randn(vocab_size, embed_dim) * 0.1
        self.W_z = np.random.randn(hidden_dim + embed_dim, hidden_dim) * 0.05
        self.W_h = np.random.randn(hidden_dim + embed_dim, hidden_dim) * 0.05
        self.W_o = np.random.randn(hidden_dim, vocab_size) * 0.05
        self.lora_rank = 8
        self.lora_A = np.zeros((hidden_dim, self.lora_rank))
        self.lora_B = np.random.randn(self.lora_rank, vocab_size) * 0.01

    def forward_step(self, token_id, h_prev):
        x = self.E[token_id % self.vocab_size, :]
        concat = np.concatenate([h_prev, x])
        z = sigmoid(np.dot(concat, self.W_z))
        h_next = (1 - z) * h_prev + z * np.tanh(np.dot(concat, self.W_h))
        logits = np.dot(h_next, self.W_o) + np.dot(np.dot(h_next, self.lora_A), self.lora_B)
        return logits, h_next
