# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import logging
from functools import lru_cache

from pydantic import BaseSettings
from pydantic import Extra


class Settings(BaseSettings):
    port: int = 6060
    host: str = '127.0.0.1'
    env: str = 'test'
    version: str = '2.2.13'

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = 'json'

    gm_queue_endpoint: str
    gm_username: str
    gm_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = Settings()
