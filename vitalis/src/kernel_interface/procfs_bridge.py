from pathlib import Path
from ...logger import logger

SIGNAL_FILE = Path("/tmp/vitalis_signal")

def read_from_kernel() -> str:
    if SIGNAL_FILE.is_file():
        try:
            data = SIGNAL_FILE.read_text().strip()
            SIGNAL_FILE.unlink()
            return data
        except Exception:
            pass
    return "STATUS: NOMINAL"

def send_to_kernel(state_report: str) -> None:
    if "IDLE" not in state_report:
        logger.info(f"[KERNEL_BRIDGE] {state_report}")
