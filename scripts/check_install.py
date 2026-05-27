import sys
from vitalis.logger import logger
from vitalis.src.brain.brain_interface import VitalisBrain
from vitalis.src.core.heartbeat_loop import HeartbeatLoop

def main():
    logger.info("=== Vitalis local smoke test start ===")
    brain = VitalisBrain()
    hb = HeartbeatLoop(brain, interval=0.5)
    hb.start()
    resp = brain.generate_response("Test protocol", "SYSTEM: TEST")
    logger.info(f"Brain response: {resp}")
    hb.stop()
    hb.join()
    logger.info("=== Smoke test finished. System Nominal. ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
