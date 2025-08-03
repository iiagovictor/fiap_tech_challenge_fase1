from datetime import datetime


class LoggerModel:

    def __init__(
        self, status_code, endpoint, message, method, type="info", latency=None
    ):
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_code = status_code
        self.endpoint = endpoint
        self.message = message
        self.type = type
        self.method = method
        self.latency = latency
