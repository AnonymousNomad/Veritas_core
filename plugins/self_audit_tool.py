def audit_state(brain, fe_engine):
    """Exposes internal brain metrics and current free-energy budget."""
    return {
        "cycle": brain.cycle,
        "temperature": brain.current_temperature,
        "free_energy": fe_engine.free_energy,
        "last_input": brain.last_input
    }
