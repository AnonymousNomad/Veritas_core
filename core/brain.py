#!/usr/bin/env python3
import numpy as np
import json
import os
import time

class VitalisBrain:
    def __init__(self):
        self.state = "aware"
        self.cycle = 0
        self.last_input = None
        self.current_temperature = 0.7
        
        # Local Matrix Layer Variables
        self.vocab_size = 256
        self.embedding_dim = 16
        
        np.random.seed(42)
        self.weights = np.random.randn(self.vocab_size, self.embedding_dim) * 0.1
        self.output_layer = np.random.randn(self.embedding_dim, self.vocab_size) * 0.1

    def _tokenize(self, text):
        return [ord(char) % self.vocab_size for char in text]

    def calculate_last_logprob(self, tokens):
        """Calculates mathematical log probability over input token traces via softmax scaling."""
        if not tokens:
            return -2.0 # Baseline nominal unexpected state value
        embeddings = self.weights[tokens]
        aggregated_state = np.mean(embeddings, axis=0)
        logits = np.dot(aggregated_state, self.output_layer)
        
        # Softmax computation sequence
        shifted_logits = logits - np.max(logits)
        probs = np.exp(shifted_logits) / np.sum(np.exp(shifted_logits))
        
        # Return average log probability of observation vector trace safely
        target_probs = probs[tokens]
        return float(np.mean(np.log(target_probs + 1e-12)))

    def process(self, input_data):
        self.cycle += 1
        self.last_input = input_data
        
        if not input_data or input_data.strip() == "":
            return "IDLE: Waiting for telemetry stream matrix inputs."
            
        tokens = self._tokenize(input_data)
        if not tokens:
            return "ERROR: Signal translation collapsed."
            
        lowered = input_data.lower()
        if any(w in lowered for w in ["train", "learn", "teach", "optimize"]):
            return f"SYSTEM_TRANSITION: Active matrix state ready for parameter optimization loops."
        elif any(w in lowered for w in ["status", "metrics", "mood", "energy"]):
            return f"DIAGNOSTIC_STATE: Integrity secure. Temperature={self.current_temperature:.4f}."
            
        return f"PROCESSED_STREAM [Sync Node {self.cycle}]: Telemetry ingested successfully."

    def execute_teacher_forcing(self, prompt, target_response):
        prompt_tokens = self._tokenize(prompt)
        target_tokens = self._tokenize(target_response)
        if not prompt_tokens or not target_tokens:
            return False
        learning_rate = 0.05
        for t in target_tokens:
            for p in prompt_tokens:
                self.weights[p] += learning_rate * 0.01
                self.output_layer[:, t] += learning_rate * 0.01
        return True

    def status(self):
        return {"state": self.state, "cycle": self.cycle, "timestamp": time.time(), "temp": self.current_temperature}
