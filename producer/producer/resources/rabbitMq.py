# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pika
from common import LoggerFactory

from producer.components.exceptions import ServiceNotAvailable
from producer.config import ConfigClass

logger = LoggerFactory('pipeline_consumer').get_logger()


class RabbitConnection:
    def __init__(self):
        pass

    def init_connection(self):
        try:
            credentials = pika.PlainCredentials(ConfigClass.gm_username, ConfigClass.gm_password)
            self._instance = pika.BlockingConnection(
                pika.ConnectionParameters(host=ConfigClass.gm_queue_endpoint, heartbeat=180, credentials=credentials)
            )
            return self._instance
        except Exception:
            logger.error('Failed to initiate rabbitMq connection')
            raise ServiceNotAvailable()

    def close_connection(self):
        self._instance.close()

    def get_current_connection(self):
        return self._instance
