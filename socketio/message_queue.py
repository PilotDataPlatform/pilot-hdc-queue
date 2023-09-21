# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pickle
from asyncio.base_events import BaseEventLoop

import aio_pika


class MessageQueue:
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        event_loop: BaseEventLoop,
        queue_name: str,
        queue_prefix: str = 'amqp://',
    ) -> None:

        """
        Summary:
            The function is basically a wrap up for aio_pika queue
            connection. It will serving to connect with designated
            queue. and fecth the message one by one
        Parameter:
            - url(str): target queue url
            - username(str): username for queue
            - password(str): password for queue
            - event_loop(str): since we ran the connect in async mode so
                add the event loop to handle it
            - queue_name(str): the queue name for the connection
            - queue_prefix(str): by default we connect to rabbitmq
        Return:
            None
        """

        self.url = url
        self.username = username
        self.password = password
        self.event_loop = event_loop
        self.queue_name = queue_name
        self.queue_prefix = queue_prefix
        self.connection = None

    async def connect(self) -> None:
        """
        Summary:
            Do the connection to the target the queue. The reason we
            dont do it in __init__ is the `aio_pika.connect_robust`
            and others are the async. we cannot make it in initialization
        Parameter:
            None
        Return:
            None
        """

        self.connection = await aio_pika.connect_robust(
            '%s%s:%s@%s/' % (self.queue_prefix, self.username, self.password, self.url), loop=self.event_loop
        )

        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name)

    async def get_message(self) -> str:
        """
        Summary:
            The function will fetch one the message from connected queue.
            And send acknowledge back to queue.
        Parameter:
            None
        Return:
            str: message from queue
        """

        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    return pickle.loads(message.body)
