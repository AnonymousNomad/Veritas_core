import threading
import time
import os
from datetime import datetime

class Dreamer:
    def __init__(self, brain, interval_sec=600):
        self.brain = brain
        self.interval = interval_sec
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.thread.join()

    def _loop(self):
        while not self._stop.is_set():
            if hasattr(self.brain, "generate_response"):
                dream = self.brain.generate_response("Internal synaptic drift consolidation sequence.", "SYSTEM: DREAM_STATE")
            elif hasattr(self.brain, "think"):
                dream = self.brain.think("SYSTEM: DREAM_STATE_TRIGGER")
            else:
                dream = "Synaptic replay executed normally."

            ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            path = os.path.expanduser(f"~/vitalis_core/storage/dreams/{ts}.txt")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(dream)
            time.sleep(self.interval)
