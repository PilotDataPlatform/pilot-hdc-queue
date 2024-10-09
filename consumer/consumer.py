# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from connection_handler import ConnectionHandler


class QueueConsumer:
    def __init__(self, routing_key, exchange_name=None, exchange_type=None, queue=None):
        self.conn = ConnectionHandler()
        self.current_conn = self.conn.get_current_connection()
        self.channel = self.current_conn.channel()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(exchange=exchange_name, queue=queue, routing_key=routing_key)
        self.exchange = exchange_name
        self.routing_key = routing_key
        self.queue = queue
