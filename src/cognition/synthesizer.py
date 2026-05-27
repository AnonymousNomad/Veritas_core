class DataSynthesizer:
    @staticmethod
    def categorize_signal(byte_count):
        if byte_count == 0:
            return "SILENT"
        elif byte_count < 64:
            return "BEACON/PROBE"
        elif byte_count < 1500:
            return "DATA_STREAM"
        else:
            return "BULK_TRANSFER"
