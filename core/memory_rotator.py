#!/usr/bin/env python3
import os
import gzip
import shutil
from datetime import datetime

class MemoryRotator:
    """
    Automated telemetry log rotation and compression engine.
    Prevents storage exhaustion during long-term continuous edge monitoring.
    """
    @staticmethod
    def inspect_and_rotate(target_file, max_bytes=5242880):  # 5MB Threshold
        if not os.path.exists(target_file):
            return
            
        if os.path.getsize(target_file) > max_bytes:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = f"{target_file}_{timestamp}.gz"
            
            print(f"\n\033[93m[SYSTEM MEMORY] Log threshold exceeded. Rotating into archive: {archive_path}\033[0m")
            try:
                with open(target_file, "rb") as f_in:
                    with gzip.open(archive_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                # Re-initialize clean tracking file
                with open(target_file, "w") as f_out:
                    f_out.write("timestamp,pulse,raw,interpretation\n")
            except Exception as e:
                print(f"\033[91m[ERROR] Security log rotation failure: {e}\033[0m")
