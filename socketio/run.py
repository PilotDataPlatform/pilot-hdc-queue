# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import asyncio
import json

from aiohttp import web
from common import configure_logging
from config import ConfigClass
from message_queue import MessageQueue
from logger import logger
import socketio

configure_logging(ConfigClass.LOGGING_LEVEL, ConfigClass.LOGGING_FORMAT)

sio = socketio.AsyncServer(cors_allowed_origins='*', engineio_logger=True, logger=True)
app = web.Application()
sio.attach(app)

loop = asyncio.get_event_loop()
mq_manager = MessageQueue(
    ConfigClass.gm_queue_endpoint, ConfigClass.gm_username, ConfigClass.gm_password, loop, 'socketio'
)


@sio.event
def connect(sid, environ):
    """
    Summary:
        SocketIO connection echo
    """
    logger.info('connect ', sid)


@sio.event
def disconnect(sid):
    """
    Summary:
        SocketIO disconnection echo
    """
    logger.info('disconnect ', sid)


async def rab_init() -> None:
    """
    Summary:
        Async function to run in the event loop. It will recieve the
        notification from rabbitqm and use socketio to send to frontend
    """

    logger.info('Start the socket io')
    await mq_manager.connect()
    while 1:
        try:
            queue_message = await mq_manager.get_message()
            if queue_message.get('method') == 'emit':
                continue

            logger.info('recieving from queue: %s', json.dumps(queue_message))
            dataset_geid = queue_message.get('payload', {}).get('dataset')
            event_type = queue_message.get('event_type', None)

            logger.info('sending to %s', dataset_geid)

            await sio.emit(event_type, queue_message, namespace='/' + dataset_geid)
        except Exception as e:
            error_message = str(e)
            logger.error('Error when processing the message: %s', error_message)


async def start_socket():
    """
    Summary:
        the socketio initialization function
    """

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=6062)
    await site.start()


##############################################################

asyncio.ensure_future(rab_init())
asyncio.ensure_future(start_socket())
loop.run_forever()
