import yaml
from pathlib import Path
DEFAULT_CONFIG = {"storage_root": str(Path.home() / "vitalis_core"), "log_file": "vitalis.log", "log_level": "INFO"}
def load_config():
    path = Path.home() / "vitalis_core" / "config.yaml"
    if path.is_file():
        with open(path, "r") as f: return {**DEFAULT_CONFIG, **yaml.safe_load(f)}
    return DEFAULT_CONFIG
