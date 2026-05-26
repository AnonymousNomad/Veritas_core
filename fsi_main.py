import threading
import time
from core.vitalis_engine import VitalisEngine
from core.brain import VitalisBrain
from core.talker import VitalisTalker
from core.handshake_module import identify_user_tier
from core.environment_manager import provision_environment
from core.mesh_network import broadcast_node_presence
from core.sovereign_shield import monitor_integrity
from src.kernel_interface.procfs_bridge import send_to_kernel, read_from_kernel
from src.senses.sigint_processor import SIGINTProcessor
from src.cognition.synthesizer import DataSynthesizer
from src.cognition.memory import MemoryBank
from src.cognition.action_engine import ActionEngine

def heartbeat_loop():
    senses = SIGINTProcessor()
    mind = DataSynthesizer()
    memory = MemoryBank()
    actions = ActionEngine()
    while True:
        system_status = read_from_kernel()
        raw_signal = senses.listen_to_traffic()
        try:
            byte_count = int(raw_signal.split()[-2]) if "bytes" in raw_signal else 0
        except:
            byte_count = 0
        interpretation = mind.categorize_signal(byte_count)
        action_taken = actions.execute(interpretation)
        memory.record("PULSE_2.0", raw_signal, interpretation)
        state_report = f"SYS: {system_status} | INT: {interpretation} | {action_taken}"
        send_to_kernel(state_report)
        time.sleep(1.0)

def main():
    print("--- FSI: Vitalis Core Sovereign Intelligence ---")
    engine = VitalisEngine()
    engine.wake_up()
    pulse = threading.Thread(target=heartbeat_loop, daemon=True)
    pulse.start()
    print("Heartbeat: Online")
    role = input("Enter Tier (kids/basic/enthusiast/professional/school): ")
    tier_config = identify_user_tier(role)
    print(f"Status: {tier_config}")
    provision_environment(role)
    broadcast_node_presence("Neuro_Nomad_Node", role)
    print(monitor_integrity("Status_Check"))
    print("--- System Fully Integrated ---")
    brain = VitalisBrain()
    talker = VitalisTalker(role)
    print("Vitalis is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Vitalis: Shutting down.")
            break
        response = brain.process(user_input)
        talker.speak(response)

if __name__ == "__main__":
    main()
