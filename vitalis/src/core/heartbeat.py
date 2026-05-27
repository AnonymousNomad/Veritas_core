def get_pulse_rate(complexity):
    """
    Calculates the operational latency based on system complexity.
    Provides the core rhythmic pulse for the organism_main loop.
    """
    # Base latency in seconds
    base_pulse = 0.5
    return base_pulse / complexity
