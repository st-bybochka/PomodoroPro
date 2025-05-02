class BaseUserException(Exception):
    status_code: int = 400
    detail: str = "User exception"

    def __str__(self) -> str:
        return self.detail


class UserAlreadyRegisteredException(BaseUserException):
    status_code = 409
    detail = "User already registered"

    def __init__(self, detail: str = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class UserNotFoundException(BaseUserException):
    status_code = 404
    detail = "User not found"


class UserIncorrectLoginOrPasswordException(BaseUserException):
    status_code = 401
    detail = "Incorrect login or password"


class UserBlockedException(BaseUserException):
    status_code = 403
    detail = "User is blocked"
