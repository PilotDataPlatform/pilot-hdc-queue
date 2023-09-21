# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
import pickle

import pika

from producer.resources.rabbitMq import RabbitConnection


def do_publish(queue, routing_key, body, exchange_name, exchange_type, binary=False):
    my_rabbit = RabbitConnection()
    connection_instance = my_rabbit.init_connection()
    channel = connection_instance.channel()
    channel.queue_declare(queue=queue)
    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
    channel.queue_bind(exchange=exchange_name, queue=queue, routing_key=routing_key)
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=pickle.dumps(body) if binary else json.dumps(body),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )
    channel.confirm_delivery()
    my_rabbit.close_connection()
