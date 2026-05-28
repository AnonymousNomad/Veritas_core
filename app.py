import subprocess
import sys

print("Ensuring dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu"])

# Now import the class
from src.core.memory_engine import MemoryEngine

if __name__ == "__main__":
    engine = MemoryEngine()
    print("Engine initialized successfully.")
