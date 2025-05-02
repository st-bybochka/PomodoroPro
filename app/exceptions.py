
class UserNotFoundException(Exception):
    detail = "User not found"


class UserNoCorrectPassword(Exception):
    detail = "User password is incorrect"


class TokenExpired(Exception):
    detail = "Token expired"


class TokenNotCorrect(Exception):
    detail = "Token is not correct"


class TaskNotFound(Exception):
    detail = "Task not found"