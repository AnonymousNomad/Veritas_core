#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

try:
    import sounddevice as sd
    _HAS_SD = True
except Exception:
    _HAS_SD = False

def _zero_crossings(sig: np.ndarray) -> int:
    return np.sum(np.abs(np.diff(np.sign(sig))) > 0)

def extract_features(duration: float = 0.5) -> tuple:
    """
    Returns (pitch_hz, rms_energy). Drops to neutral 0.0 defaults if hardware bindings are missing.
    """
    if not _HAS_SD:
        return 0.0, 0.0

    try:
        samplerate = 16000
        raw = sd.rec(int(duration * samplerate), samplerate=samplerate,
                     channels=1, dtype='float32', blocking=True).flatten()
        energy = float(np.sqrt(np.mean(raw ** 2)))
        zc = _zero_crossings(raw)
        pitch = float(zc * (1.0 / duration) / 2.0)
        return pitch, energy
    except Exception:
        return 0.0, 0.0
