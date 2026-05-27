#!/usr/bin/env python3
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.brain import VitalisBrain
from extensions.dreamer import Dreamer
from extensions.temp_scheduler import TemperatureScheduler
from src.energy.free_energy import FreeEnergyEngine

def main():
    print("[*] Launching Vitalis Bio-AI Engine with Active Inference (FEP)...")
    brain = VitalisBrain()
    temp_scheduler = TemperatureScheduler(brain)
    fe_engine = FreeEnergyEngine(alpha=0.85)
    
    dreamer = Dreamer(brain, interval_sec=600)
    dreamer.start()
    
    print("[+] Engine operational. Free-Energy optimization loops tracking live telemetry.")
    print("Telemetry In > ", end="")
    
    while True:
        try:
            user_input = input().strip()
            if not user_input:
                print("Telemetry In > ", end="")
                continue
            if user_input.lower() in ["exit", "quit"]:
                dreamer.stop()
                break
            
            tokens = brain._tokenize(user_input)
            logprob = brain.calculate_last_logprob(tokens)
            fe_engine.ingest_observation(logprob)
            brain.current_temperature = fe_engine.temperature_factor(base_temp=0.8)
            temp_scheduler.tick()
            response = brain.process(user_input)
            print(f"Metrics Out > {response} [FE: {fe_engine.free_energy:.4f} | Temp: {brain.current_temperature:.4f}]\nTelemetry In > ", end="")
        except (KeyboardInterrupt, EOFError):
            dreamer.stop()
            break

if __name__ == "__main__":
    main()
