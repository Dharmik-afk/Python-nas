from datetime import datetime

class SystemState:
    def __init__(self):
        self.start_time = datetime.now()
        self.services = {
            "copyparty": "unknown",
            "fastapi": "unknown"
        }

state = SystemState()