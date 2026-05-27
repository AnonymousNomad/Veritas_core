#!/usr/bin/env python3
# -*- coding: utf-8 -*-

_POSITIVE = {"good", "great", "awesome", "nice", "love", "excellent", "happy", "fantastic", "nominal", "secure"}
_NEGATIVE = {"bad", "terrible", "hate", "awful", "sad", "angry", "worst", "pain", "attack", "compromise"}

def sentiment_score(text: str) -> float:
    """
    Computes strict text-token sentiment metrics returning float bounded in [-1, 1].
    """
    tokens = set(word.strip('.,!?()[]"\'').lower() for word in text.split())
    pos = len(tokens & _POSITIVE)
    neg = len(tokens & _NEGATIVE)

    if pos == 0 and neg == 0:
        return 0.0
    return (pos - neg) / max(pos + neg, 1)
