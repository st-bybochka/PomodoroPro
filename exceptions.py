class UserNotFoundException(Exception):
    detail = "User not found"


class UserNoCorrectPassword(Exception):
    detail = "User password is incorrect"