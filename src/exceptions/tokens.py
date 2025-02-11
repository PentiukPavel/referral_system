from core.choices import APIMessages


class TokenAlreadyExists(Exception):
    def __init__(self):
        message = APIMessages.TOKEN_ALREADY_EXISTS.value
        super().__init__(message)


class TokenDoesNotExist(Exception):
    def __init__(self):
        message = APIMessages.TOKEN_DOES_NOT_EXIST.value
        super().__init__(message)


class WrongToken(Exception):
    def __init__(self):
        message = APIMessages.WRONG_TOKEN.value
        super().__init__(message)
