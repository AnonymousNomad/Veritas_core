#!/usr/bin/env python3
import time
import sys
import select
import os
from core.brain import VitalisBrain
from core.template_manager import TemplateManager
from core.memory_rotator import MemoryRotator

def main_loop():
    brain = VitalisBrain()
    pm = TemplateManager()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(base_dir, "vitalis_memory.csv")
    
    # Ensure tracking metrics file exists
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("timestamp,pulse,raw,interpretation\n")

    print("[+] Vitalis Bio-Digital Core Online. Press Ctrl+C to terminate.")
    print("[+] Dynamic Posture Profiles Loaded. Processing non-blocking telemetry stream...\n")
    
    while True:
        # Load profile configurations dynamically each cycle
        profile = pm.load_active_profile()
        color = profile.get("color_code", "\033[94m")
        mode = profile.get("mode", "MONITORING")
        reset = "\033[0m"
        
        # Continuous clean broadcast terminal heartbeat
        sys.stdout.write(f"{color}Broadcast: SYS: STATUS: NOMINAL | INT: ACTIVE | ACTION: {mode}{reset}\r")
        sys.stdout.flush()
        
        # Non-blocking check for user terminal input (waits 1 second per cycle)
        ready, _, _ = select.select([sys.stdin], [], [], 1.0)
        if ready:
            user_input = sys.stdin.readline().strip()
            if user_input:
                print(f"\n\n[SENSORY INGEST] Processing incoming payload: '{user_input}'")
                try:
                    # Dynamically inject template complexity limitations into core brain
                    brain.max_complexity = profile.get("max_complexity", 5)
                    result = brain.classify_input(user_input)
                    print(f"[METRIC RESPONSE] {result}\n")
                except AttributeError:
                    print(f"[METRIC RESPONSE] Stream received. Core logic processed raw bytes.\n")
                
                # Append raw trace locally for data retention tracking
                with open(log_file, "a") as f:
                    f.write(f"{time.time()},{profile.get('max_complexity')},{user_input},{mode}\n")
                
                # Enforce storage safety validation checks
                MemoryRotator.inspect_and_rotate(log_file)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n\n\033[93m[-] Sovereign Core safely detached.\033[0m")
