class UsageClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class NetworkError(UsageClientError):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f'{{"error": "{self.message}","status_code": "{self.status_code}"}}'

class ValidationError(UsageClientError):
    def __init__(self, field_name, message="Validation error"):
        self.field_name = field_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{{"error": "{self.message}", "field": "{self.field_name}"}}'
