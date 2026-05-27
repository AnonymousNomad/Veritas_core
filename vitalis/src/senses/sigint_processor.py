import socket
from ...logger import logger

class SIGINTProcessor:
    @staticmethod
    def listen_to_traffic():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.settimeout(1.0)
            packet = s.recvfrom(65565)
            return f"SIGNAL_DETECTED: {len(packet[0])} bytes"
        except Exception:
            return "SIGNAL_SILENT"
