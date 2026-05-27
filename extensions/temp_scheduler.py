class TemperatureScheduler:
    def __init__(self, brain):
        self.brain = brain
        self.adrenaline = 0.5
        self.cortisol = 0.3
        self.base_temp = 0.8

    def tick(self):
        self.adrenaline = max(0.1, self.adrenaline - 0.01)
        self.cortisol = max(0.1, self.cortisol - 0.005)
        computed_temp = self.base_temp * (1.0 + (0.3 * self.adrenaline) - (0.1 * self.cortisol))
        target_temp = max(0.4, min(1.4, computed_temp))
        if hasattr(self.brain, "current_temperature"):
            self.brain.current_temperature = target_temp
