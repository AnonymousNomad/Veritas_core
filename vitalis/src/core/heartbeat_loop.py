import time
import threading
from ...logger import logger
from ..kernel_interface.procfs_bridge import send_to_kernel, read_from_kernel
from ..senses.sigint_processor import SIGINTProcessor

class HeartbeatLoop(threading.Thread):
    def __init__(self, brain, interval: float = 1.0):
        super().__init__(daemon=True)
        self.brain = brain
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self):
        senses = SIGINTProcessor()
        logger.info(f"Heartbeat loop started (interval={self.interval}s)")
        
        while not self._stop_event.is_set():
            status = read_from_kernel()
            raw_signal = senses.listen_to_traffic()
            action = "ACTION: MONITORING" if "SIGNAL_DETECTED" in raw_signal else "ACTION: IDLE"
            
            state_report = f"SYS: {status} | SENSE: {raw_signal} | {action}"
            send_to_kernel(state_report)
            time.sleep(self.interval)

    def stop(self):
        self._stop_event.set()
