# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from functools import lru_cache
from typing import Any
from typing import Dict
from typing import Optional

from common import VaultClient
from pydantic import BaseSettings
from pydantic import Extra


class VaultConfig(BaseSettings):
    """Store vault related configuration."""

    APP_NAME: str = 'service_queue'
    CONFIG_CENTER_ENABLED: bool = False

    VAULT_URL: Optional[str]
    VAULT_CRT: Optional[str]
    VAULT_TOKEN: Optional[str]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    config = VaultConfig()

    if not config.CONFIG_CENTER_ENABLED:
        return {}

    client = VaultClient(config.VAULT_URL, config.VAULT_CRT, config.VAULT_TOKEN)
    return client.get_from_vault(config.APP_NAME)


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'service_queue'
    port: int = 6060
    host: str = '127.0.0.1'
    env: str = 'test'
    namespace: str = 'greenroom'

    CONFIG_CENTER_ENABLED: bool = False
    VAULT_URL: str
    VAULT_CRT: str
    VAULT_TOKEN: str

    # greenroom queue
    gm_queue_endpoint: str
    gm_username: str
    gm_password: str

    # folders been watched
    data_lake: str
    claim_name: str = ''

    # data_transfer pipeline
    data_transfer_image: str = ''
    bids_validate_image: str = ''

    # data_transfer pipeline
    copy_pipeline: str = ''
    copy_pipeline_folder: str = ''
    move_pipeline: str = ''
    move_pipeline_folder: str = ''
    bids_validate_pipeline: str = ''

    # greenroom queue
    gr_queue: str = ''
    gr_exchange: str = ''

    OPEN_TELEMETRY_ENABLED: bool = False
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    GREEN_ZONE_LABEL: str
    CORE_ZONE_LABEL: str
    NFS_MOUNT: str
    RDS_DBNAME: str
    RDS_HOST: str
    RDS_PORT: str = ''
    S3_HOST: str
    S3_PORT: str = ''
    S3_INTERNAL_HTTPS: str
    DATAOPS_SERVICE: str
    DATASET_SERVICE: str
    QUEUE_SERVICE: str
    METADATA_SERVICE: str
    PROJECT_SERVICE: str
    APPROVAL_SERVICE: str
    NOTIFICATION_SERVICE: str
    KAFKA_URL: str
    REDIS_HOST: str
    REDIS_PORT: str
    ATLAS_HOST: str
    ATLAS_PORT: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return env_settings, load_vault_settings, init_settings, file_secret_settings


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = get_settings()
