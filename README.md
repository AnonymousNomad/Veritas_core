---
license: gpl-3.0
language:
- en
tags:
- synthetic-intelligence
- cybersecurity
- sovereign-ai
- open-source
---

# FSI Vitalis CyberCore
### Ferrell Synthetic Intelligence (FSI)
**Built by Neuro_Nomad**

---

## The FSI Manifesto: Sovereignty Through Synthetic Logic

The era of monitored, centralized digital existence is changing.
The future of synthetic intelligence belongs to the individuals
who build, own and defend their own cognitive infrastructure.

**I. The Mandate of Sovereignty**
True intelligence thrives without surveillance. Any system requiring
persistent corporate connectivity compromises your autonomy. FSI exists
to facilitate the reclamation of intellectual ownership. We build for
the architect, the operator and the independent developer.
We don't provide a service. We provide a foundation.

**II. Architecture as Ethics**
Our code reflects our values. By prioritizing minimal dependencies
and local performance, we ensure your cognitive chain remains unbroken
by third-party intervention. To build with FSI is to commit to
technical integrity.

**III. The Frontier of Synthetic Logic**
We are architects of human-machine symbiosis built on transparency
and ownership. We believe safety and sovereignty are not opposites.
A truly sovereign system is also a responsible one. FSI is the
structural answer to a world that concentrates too much intelligence
in too few hands.

**IV. The Operational Vow**
We build because we believe developers deserve better.
We build because privacy is a right.
We build because the tools you use should belong to you.

---

## What This Is
A demonstration fork of Vitalis Core showing what the base model
becomes when directed toward a specific domain.
This is not a finished product. It is not a tool.
It is proof of concept — showing developers what they can build.

---

## What It Does
- Classifies input as threats, defensive actions, queries or signals
- Assigns severity — HIGH, MEDIUM, LOW
- Assigns confidence scores to every classification
- Logs everything to an immutable JSON-Lines audit trail
- Config-driven — edit keywords without touching code

---

## Benchmark Results
- malware detected → THREAT_DETECTED [HIGH] — Confidence: 0.9
- monitor the network → DEFENSIVE_ACTION — Confidence: 0.6
- what is a port scan → THREAT_DETECTED [LOW] — Confidence: 0.7
- unauthorized access → THREAT_DETECTED [MEDIUM] — Confidence: 0.85
- harden the firewall → DEFENSIVE_ACTION — Confidence: 0.6

Tests: All passing.

---

## Run It
python3 fsi_main.py

## Run Tests
python3 tests/test_brain.py

---

## Base Model
Built on Vitalis Core — FSI open source sovereign intelligence framework.
huggingface.co/FerrellSyntheticIntelligence/Vitalis_Core

---

## Who Built This
Self-taught developer. No degree. No corporate backing. No team.
One person. One tablet. One mission.
Sovereign intelligence belongs to the people.

---

## License
GPL-3.0
