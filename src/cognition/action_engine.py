class ActionEngine:
    @staticmethod
    def execute(interpretation):
        if interpretation == "BULK_TRANSFER":
            # You can customize this logic for any automated action
            return "ACTION: LOG_ANOMALY_TRIGGERED"
        elif interpretation == "BEACON/PROBE":
            return "ACTION: MONITORING_ACTIVE"
        return "ACTION: IDLE"
