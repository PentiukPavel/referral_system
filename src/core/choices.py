from enum import StrEnum


class APIMessages(StrEnum):
    NOT_FOUND = "Not Found."
    TOKEN_ALREADY_EXISTS = "Token already exists."
    TOKEN_DOES_NOT_EXIST = "Active token does not exist."
