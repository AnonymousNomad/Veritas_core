import time

def get_pulse_rate(complexity_factor):
    """
    Returns a float representing the 'pulse' delay in seconds.
    Higher complexity slows the pulse, mimicking deep processing.
    """
    base_pulse = 1.0
    return base_pulse / (complexity_factor * 0.5)
