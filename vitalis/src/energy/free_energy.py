import math
from ...logger import logger

class FreeEnergyEngine:
    def __init__(self, alpha: float = 0.85):
        self.alpha = alpha
        self.free_energy = 0.0

    def ingest_observation(self, model_pred_logprob: float) -> None:
        self.free_energy = self.alpha * self.free_energy + (1 - self.alpha) * (-model_pred_logprob)
        logger.debug(f"Free-energy updated: {self.free_energy:.4f}")

    def temperature_factor(self, base_temp: float = 0.8) -> float:
        factor = 1.0 + 0.5 * math.tanh(self.free_energy - 1.0)
        return max(0.4, min(1.4, base_temp * factor))
