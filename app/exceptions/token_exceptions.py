class TokenNotCorrectException(Exception):
    status_code = 401
    detail = 'Token is not correct'


class TokenMissingException(Exception):
    status_code = 401
    detail = 'Token is missing'