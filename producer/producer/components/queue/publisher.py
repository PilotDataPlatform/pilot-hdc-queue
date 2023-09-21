# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Optional

from common import LoggerFactory

from producer.components.exceptions import ServiceNotAvailable
from producer.components.schemas import BasePayload
from producer.config import ConfigClass
from producer.resources.queuePublisher import MessagePublish

logger = LoggerFactory('pipeline_publisher').get_logger()


class BasedProducer:
    def __init__(self, event_type: str, project: Optional[str], create_time: float, payload: BasePayload):
        self.event_type = event_type
        self.project = project
        self.create_time = create_time
        self.routing_key = project + '.' + event_type
        self.payload = payload
        self.producer = MessagePublish(
            self.routing_key, exchange_name=ConfigClass.gr_exchange, exchange_type='topic', queue=ConfigClass.gr_queue
        )

    def publish(self):
        logger.info(f'{self.routing_key}  ---------event sending.')
        try:
            self.producer.publish(self.payload)
            return 'Succeed'
        except ServiceNotAvailable as e:
            logger.error(f'Error when trying to parse the message to queue: {e}')
            raise ServiceNotAvailable()
