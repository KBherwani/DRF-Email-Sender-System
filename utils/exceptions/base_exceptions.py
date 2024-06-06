"""
Module containing a base exception class with data attributes for item and message.
This class is intended for use in situations where additional context or logging information
is needed when handling exceptions.

Classes:
- BaseExceptionWithLogs: A frozen data class inheriting from the built-in Exception class.
"""

from dataclasses import dataclass

from rest_framework import status


@dataclass(frozen=True)
class APIBaseException(Exception):
    item: str
    message: str
    status_code: int = status.HTTP_400_BAD_REQUEST

    def error_data(self) -> dict:
        error_data = {"item": self.item, "message": self.message}
        return error_data

    def __str__(self):
        return "{}: {}".format(self.item, self.message)


class Status403Exception(APIBaseException):
    def __init__(self, item, message):
        super().__init__(item, message, status_code=status.HTTP_403_FORBIDDEN)


class Status404Exception(APIBaseException):
    def __init__(self, item, message):
        super().__init__(item, message, status_code=status.HTTP_404_NOT_FOUND)
