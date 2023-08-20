class UsageClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NetworkError(UsageClientError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ValidationError(UsageClientError):
    def __init__(self, field_name, message="Validation error"):
        self.field_name = field_name
        self.message = message
        super().__init__(self.message)
