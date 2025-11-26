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
    """Store service configuration settings."""

    APP_NAME: str = 'service_queue'
    version: str = '2.2.13'
    port: int = 6060
    host: str = '0.0.0.0'
    env: str = 'test'

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = 'json'

    gm_queue_endpoint: str
    gm_username: str
    gm_password: str
    # pipeline name
    copy_pipeline: str
    move_pipeline: str
    # greenroom queue
    gr_queue: str
    gr_exchange: str

    OPEN_TELEMETRY_ENABLED: str = 'FALSE'
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = get_settings()
