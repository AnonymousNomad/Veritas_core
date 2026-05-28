import sys
import subprocess
try:
    import faiss
    print("FAISS verified.")
except ImportError:
    print("FAISS missing, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faiss-cpu"])
    import faiss

from src.core.memory_engine import MemoryEngine
# Rest of your app code follows here
