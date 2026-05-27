#!/usr/bin/env python3
import math

class FreeEnergyEngine:
    def __init__(self, alpha: float = 0.85):
        self.alpha = alpha
        self.free_energy = 0.0
        self.prediction_error = 0.0
        self.history = []

    def ingest_observation(self, model_pred_logprob: float):
        """
        Calculates variational surprise from prediction log probabilities.
        Surprisal = -log p(obs | internal state)
        """
        self.prediction_error = -model_pred_logprob
        # Exponential moving average tracking state bounds
        self.free_energy = (self.alpha * self.free_energy) + ((1.0 - self.alpha) * self.prediction_error)
        self.history.append(self.free_energy)

    def apply_pressure(self, delta: float):
        """Allows direct structural manipulation via internal electron execution packages."""
        self.free_energy = max(0.0, self.free_energy + delta)

    def temperature_factor(self, base_temp: float = 0.8) -> float:
        """Maps free energy via hyperbolic tangent mapping to range [0.4, 1.4]"""
        factor = 1.0 + 0.5 * math.tanh(self.free_energy - 1.0)
        return max(0.4, min(1.4, base_temp * factor))
