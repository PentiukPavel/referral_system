from enum import StrEnum


class APIMessages(StrEnum):
    ALREADY_REFERRED = "You already have used this code."
    NOT_SELF = "You can not refer to yourself."
    NOT_FOUND = "Not Found."
    REFERRED_SUCCESSFULLY = "Referred successfully."
    TOKEN_ALREADY_EXISTS = "Token already exists."
    TOKEN_DOES_NOT_EXIST = "Active token does not exist."
    WRONG_TOKEN = "Code does not exist or expired."
