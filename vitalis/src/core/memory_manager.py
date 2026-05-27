import json

def load_identity():
    """
    Retrieves the system identity from the secure local store.
    Ensures persistent contextual awareness across operational cycles.
    """
    try:
        with open('core/identity.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"user_name": "Unknown", "alias": "Nomad"}
