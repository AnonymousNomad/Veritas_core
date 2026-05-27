import json
import os
import shutil

BASE_PATH = os.path.expanduser("~/vitalis_core")

def get_free_space():
    usage = shutil.disk_usage(BASE_PATH)
    return usage.free

def load_identity():
    identity_path = os.path.join(BASE_PATH, "core/identity.json")
    with open(identity_path, 'r') as f:
        return json.load(f)

def store_memory(data):
    memory_path = os.path.join(BASE_PATH, "memory_store.json")
    
    if get_free_space() < 100 * 1024 * 1024:
        if os.path.exists(memory_path):
            with open(memory_path, 'r') as f:
                lines = f.readlines()
            if len(lines) > 1:
                with open(memory_path, 'w') as f:
                    f.writelines(lines[1:])
    
    w
