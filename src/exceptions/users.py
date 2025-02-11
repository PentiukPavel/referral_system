from core.choices import APIMessages


class NotSelf(Exception):
    def __init__(self):
        message = APIMessages.NOT_SELF.value
        super().__init__(message)


class AlreadyReferred(Exception):
    def __init__(self):
        message = APIMessages.ALREADY_REFERRED.value
        super().__init__(message)
