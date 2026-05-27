import csv
from datetime import datetime

class MemoryBank:
    def __init__(self, log_file="vitalis_memory.csv"):
        self.log_file = log_file

    def record(self, pulse, raw, interpretation):
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), pulse, raw, interpretation])
