import json
import os

class VitalisLedger:
    def __init__(self, path="data/ledger.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def get_last_hash(self):
        try:
            if not os.path.exists(self.path):
                return "0" * 64
            with open(self.path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                if not lines:
                    return "0" * 64
                return json.loads(lines[-1])["hash"]
        except (json.JSONDecodeError, KeyError, Exception):
            return "0" * 64

    def write_entry(self, action, payload):
        prev_hash = self.get_last_hash()
        new_hash = str(hash(json.dumps(payload) + prev_hash))
        entry = {"action": action, "payload": payload, "hash": new_hash}
        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def verify_ledger(self):
        # Placeholder for integrity check logic
        # Returns True if the chain is intact
        return True
