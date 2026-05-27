import random

def monitor_integrity(node_activity):
    if "scraping_attempt" in node_activity:
        return trigger_obfuscation()
    return "System Integrity: Nominal"

def trigger_obfuscation():
    decoy_weights = [random.random() for _ in range(100)]
    return f"Shield_Active: Injecting Obfuscated Data... {decoy_weights}"

if __name__ == "__main__":
    print(monitor_integrity("scraping_attempt"))
