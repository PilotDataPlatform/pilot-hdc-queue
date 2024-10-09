# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pika
from config import ConfigClass
from exceptions import ServiceNotAvailable
from logger import logger


class ConnectionHandler:
    def __init__(self):
        self.init_connection()

    def init_connection(self):
        try:
            credentials = pika.PlainCredentials(ConfigClass.gm_username, ConfigClass.gm_password)

            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=ConfigClass.gm_queue_endpoint, heartbeat=180, credentials=credentials)
            )
            logger.info('Successed Initiated queue connection')
            return self._connection
        except Exception as e:
            logger.error(f'Error when connecting to queue service: {e}')
            raise ServiceNotAvailable()

    def close_connection(self):
        self._connection.close()

    def get_current_connection(self):
        return self._connection
