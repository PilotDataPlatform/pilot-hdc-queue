# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from http.client import UNPROCESSABLE_ENTITY

from producer.components.exceptions import ServiceException


class ValidateException(ServiceException):
    """Raised when unhandled/unexpected internal error occurred."""

    def __init__(self, error: str, *args, **kwargs) -> None:
        self.error = error

    @property
    def status(self) -> int:
        return UNPROCESSABLE_ENTITY

    @property
    def code(self) -> str:
        return 'unprocessable_entity'

    @property
    def details(self) -> str:
        return f'Missing required {self.error}'
