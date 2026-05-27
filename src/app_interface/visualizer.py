import json
from src.core.heartbeat_engine import get_pulse_rate

class TelemetryVisualizer:
    """
    Translates raw core heartbeat into UI-ready visual data.
    """
    @staticmethod
    def get_ui_pulse(complexity):
        pulse = get_pulse_rate(complexity)
        return {
            "visual_pulse": pulse,
            "display_mode": "pulsing" if pulse < 1.5 else "deep_thought"
        }
