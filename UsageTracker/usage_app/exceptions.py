class UsageAppError(Exception):
    pass

class NetworkError(UsageAppError):
    pass

class ValidationError(UsageAppError):
    pass
