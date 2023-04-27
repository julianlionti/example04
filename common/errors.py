from common import AppException


class BadRequest(AppException):
    def __init__(self, message="Bad request", payload=None):
        super().__init__(message=message, status_code=400, payload=payload)


class NotFound(AppException):
    def __init__(self, message="Not found", payload=None):
        super().__init__(message=message, status_code=404, payload=payload)


class Unauthorized(AppException):
    def __init__(self, message="Unauthorized", payload=None):
        super().__init__(message=message, status_code=401, payload=payload)


class Forbidden(AppException):
    def __init__(self, message="Forbidden", payload=None):
        super().__init__(message=message, status_code=403, payload=payload)


class InternalServerError(AppException):
    def __init__(self, message="Internal server error", payload=None):
        super().__init__(message=message, status_code=500, payload=payload)
