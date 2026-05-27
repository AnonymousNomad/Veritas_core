#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

class SelfModel:
    """
    Maintains and updates the system's running model of conversation dynamics.
    Persists data cleanly locally to survive physical power cycles.
    """
    def __init__(self, path: Path = None):
        if path is None:
            self.path = Path(__file__).parent.parent.parent / "storage" / "self_model.json"
        else:
            self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        self.state = {
            "stress": 0.0,
            "confidence": 0.5,
            "engagement": 0.5,
            "last_emotion": "neutral"
        }
        self._load()

    def _load(self):
        if self.path.is_file():
            try:
                with open(self.path, "r") as f:
                    self.state.update(json.load(f))
            except Exception:
                pass

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    def update(self, pitch: float, energy: float, sentiment: float):
        alpha = 0.2  # EMA factor variable step bounds

        norm_pitch = max(0.0, min(1.0, (pitch - 80) / (300 - 80))) if pitch > 0 else 0.5
        norm_energy = max(0.0, min(1.0, energy / 0.1)) if energy > 0 else 0.3

        self.state["stress"] = (1 - alpha) * self.state["stress"] + alpha * (1.0 - (norm_pitch * 0.6 + norm_energy * 0.4))
        self.state["confidence"] = (1 - alpha) * self.state["confidence"] + alpha * ((sentiment + 1) / 2)
        self.state["engagement"] = (1 - alpha) * self.state["engagement"] + alpha * norm_energy

        if sentiment > 0.3:
            self.state["last_emotion"] = "positive"
        elif sentiment < -0.3:
            self.state["last_emotion"] = "negative"
        else:
            self.state["last_emotion"] = "neutral"

        self.save()

    def as_prompt_modifier(self) -> str:
        mood = []
        if self.state["stress"] > 0.6:
            mood.append("STRESSED")
        if self.state["confidence"] < 0.4:
            mood.append("UNCERTAIN")
        if self.state["engagement"] > 0.7:
            mood.append("ENGAGED")
        if not mood:
            mood.append("NOMINAL_NEUTRAL")
        return f"[AFFECTIVE_POSTURING_SIGNAL: {', '.join(mood)}]"
