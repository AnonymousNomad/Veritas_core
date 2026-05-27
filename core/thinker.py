import time
import json
import os

BASE_PATH = os.path.expanduser("~/vitalis_core")

def emit_thought(thought_content, status="active"):
    telemetry = {
        "timestamp": time.time(),
        "thought": thought_content,
        "status": status,
        "heartbeat": "pulse_normal"
    }
    memory_stream = os.path.join(BASE_PATH, "memory_stream.jsonl")
    with open(memory_stream, "a") as f:
        f.write(json.dumps(telemetry) + "\n")

if __name__ == "__main__":
    emit_thought("Initializing conscious state...")
