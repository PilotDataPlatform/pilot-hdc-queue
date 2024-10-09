# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import APIRouter

from producer.components.queue.schemas import SendMessageRequestSchema
from producer.components.queue.schemas import SendMessageResponseSchema
from producer.components.schemas import EAPIResponseCode
from producer.logger import logger

from .models import trigger_event

router = APIRouter(tags=['Send Message Service'])


@router.post(
    '/send_message',
    summary='Send message to queue consumer to trigger pipelines',
    response_model=SendMessageResponseSchema,
)
def send_message(data: SendMessageRequestSchema):
    res = SendMessageResponseSchema()
    event_type = data.get('event_type', None)
    payload = data.get('payload', None)
    create_time = data.get('create_timestamp', None)
    project = payload.get('project', '')
    logger.info(f'postData is : {data}')
    try:
        res.result = trigger_event(event_type, project, create_time, payload)
        return res.json_response()
    except Exception as e:
        res.code = EAPIResponseCode.internal_error
        res.error_msg = str(e)
        return res.json_response()
