import json
import time

def broadcast_state(thought_data, pulse_rate, training_status=None):
    """
    Serializes internal state and training status for visual heartbeat.
    """
    telemetry = {
        "timestamp": time.time(),
        "pulse": pulse_rate,
        "cognitive_state": thought_data,
        "training_active": training_status is not None,
        "training_module": training_status
    }
    return json.dumps(telemetry)
