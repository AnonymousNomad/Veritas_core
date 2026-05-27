#!/usr/bin/env python3
import json
import os

class TemplateManager:
    """
    Sovereign profile configuration engine for Vitalis_Core.
    Handles runtime adjustments for targeted security posture profiles.
    """
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.profile_path = os.path.join(self.base_dir, "storage", "user_profiles.json")

    def load_active_profile(self) -> dict:
        try:
            with open(self.profile_path, "r") as f:
                data = json.load(f)
                active = data.get("active_profile", "cybersecurity_recon")
                return data["profiles"].get(active, {})
        except Exception:
            # Safe architectural fallback state
            return {"mode": "DEFAULT", "max_complexity": 5, "response_bias": 0.5, "color_code": "\033[94m"}
