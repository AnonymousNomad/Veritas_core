import logging, sys
from pathlib import Path
from .config import load_config
cfg = load_config()
logging.basicConfig(level=cfg["log_level"], format="%(asctime)s %(levelname)s %(message)s", 
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("vitalis")
