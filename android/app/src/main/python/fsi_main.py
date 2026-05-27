from core.vitalis_engine import VitalisEngine
from core.handshake_module import identify_user_tier
from core.environment_manager import provision_environment
from core.mesh_network import broadcast_node_presence
from core.sovereign_shield import monitor_integrity

def main():
    print("--- FSI: Vitalis Core Sovereign Intelligence ---")
    engine = VitalisEngine()
    engine.wake_up()
    role = input("Enter Tier (kids/basic/enthusiast/professional/school): ")
    tier_config = identify_user_tier(role)
    print(f"Status: {tier_config}")
    env = provision_environment(role)
    broadcast_node_presence("Neuro_Nomad_Node", role)
    print(monitor_integrity("Status_Check"))
    print("--- System Fully Integrated ---")

if __name__ == "__main__":
    main()
