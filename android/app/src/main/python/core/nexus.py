import sys
import os
sys.path.append(os.path.expanduser("~/vitalis_core"))
from core.memory_manager import store_memory

def route_thought(data):
    store_memory({"type": "particle", "content": data})
