# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import time

from common import LoggerFactory
from fastapi import APIRouter

from producer.components.broker.schemas import PublishBrokerRequestSchema
from producer.components.broker.schemas import PublishBrokerResponseSchema
from producer.components.schemas import EAPIResponseCode

from .publish import do_publish

logger = LoggerFactory('pipeline_publisher').get_logger()
router = APIRouter(prefix='/broker', tags=['Message Broker Service'])


@router.post('/pub', summary='Publish the message to broker', response_model=PublishBrokerResponseSchema)
def publish_broker(data: PublishBrokerRequestSchema):
    res = PublishBrokerResponseSchema()
    event = data.dict()

    logger.info(event)

    queue = event.get('queue')
    routing_key = event.get('routing_key')
    exchange = event.get('exchange', {'name': 'FANOUT_TOPIC', 'type': 'fanout'})

    required = ['name', 'type']
    for field in required:
        if field not in exchange:
            res.code = EAPIResponseCode.bad_request
            res.error_msg = "param '{}' is required in exchange object.".format(field)
            return res.json_response()

    create_timestamp = event.get('create_timestamp', time.time())
    event['create_timestamp'] = create_timestamp
    event['exchange'] = exchange

    do_publish(
        queue,
        routing_key,
        event,
        exchange_name=exchange['name'],
        exchange_type=exchange['type'],
        binary=event.get('binary', False),
    )
    logger.info('Published successfully')

    res.code = EAPIResponseCode.success
    res.result = event
    return res.json_response()
