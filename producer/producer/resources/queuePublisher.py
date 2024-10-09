# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json

import pika

from producer.components.exceptions import ServiceNotAvailable
from producer.components.exceptions import UnhandledException
from producer.logger import logger

from .queueConnector import ConnectionHandler


class MessagePublish:
    """Publish message, and declare queue's channel and exchange binding."""

    def __init__(self, routing_key, exchange_name=None, exchange_type=None, queue=None):
        self.conn = ConnectionHandler()
        self.current_conn = self.conn.get_current_connection()
        self.channel = self.current_conn.channel()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(exchange=exchange_name, queue=queue, routing_key=routing_key)
        self.exchange = exchange_name
        self.routing_key = routing_key

    def publish(self, body):
        """Publish message to the queue by defined exchange, routing key and message body."""
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
            logger.info(f'[x] Sent {body!r}')
            self.channel.confirm_delivery()
            self.conn.close_connection()
            logger.info(
                f'[x] Message has been confirmed \
                as received {body}'
            )
            logger.info('Sent Message successfully to the queue')
        except pika.exceptions.UnroutableError:
            logger.error(f'Failed to send message {body!r}')
            raise ServiceNotAvailable()
        except Exception as e:
            logger.error(f'Unexpected exception while message delivery: {e}')
            raise UnhandledException()
