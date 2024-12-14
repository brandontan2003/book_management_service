class ApiResponsePayload:
    def __init__(self, status, result):
        self.status = status
        self.result = result

    def to_json(self):
        return {
            "status": self.status,
            "result": self.result
        }
