# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
import os
import time

from common import configure_logging
from config import ConfigClass
from config import get_settings
from logger import logger
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pipelines.bids_validate import bids_validate_pipeline
from pipelines.data_copy import folder_copy_pipeline
from pipelines.data_delete import folder_delete_pipeline

from consumer import QueueConsumer


def millis():
    current_milli_time = str(round(time.time() * 1000))

    return current_milli_time


def bids_validator(ch, method, message):
    try:
        logger.info(f'bids_validate message has been received: {message}')
        dataset_code = message['dataset_code']
        access_token = message['access_token']
        try:
            bids_validate_pipeline(logger, dataset_code, access_token)
            logger.info('bids_validate pipeline is processing')
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.exception(f'Error occurred while validate bids dataset. {e}')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as e:
        logger.exception(f'Error occurred while validate bids dataset. {e}')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def folder_copy(ch, method, message):
    try:
        logger.info(f'folder_copy message has been received: {message}')
        source_geid = message['source_geid']
        destination_geid = message['destination_geid']
        request_info = message.get('request_info')
        include_geids = message['include_geids']
        access_token = message['access_token']
        folder_copy_pipeline(
            logger,
            source_geid,
            destination_geid,
            method.routing_key.split('.')[0],
            request_info,
            include_geids,
            message,
            access_token,
        )
        logger.info('folder_copy pipeline is processing')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.exception(f'Error occurred while copying file {e}')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def folder_delete(ch, method, message):
    try:
        logger.info(f'folder_delete message has been received: {message}')
        source_geid = message['source_geid']
        include_geids = message['include_geids']
        access_token = message['access_token']
        folder_delete_pipeline(
            logger, source_geid, method.routing_key.split('.')[0], include_geids, message, access_token
        )
        logger.info('folder_delete pipeline is processing')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.exception(f'Error occurred while moving file. {e}')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def callback(ch, method, properties, body):
    """Received message and start to consume message."""

    logger.info(f'[x] Received {body!r}')
    message = json.loads(body)

    if method.routing_key.split('.')[-1] == 'bids_validate':
        bids_validator(ch, method, message)

    elif method.routing_key.split('.')[-1] == 'folder_copy':
        folder_copy(ch, method, message)

    elif method.routing_key.split('.')[-1] == 'folder_delete':
        folder_delete(ch, method, message)

    else:
        logger.exception('Undefined Routing key')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    consumer = QueueConsumer(
        routing_key='#', exchange_name=ConfigClass.gr_exchange, exchange_type='topic', queue=ConfigClass.gr_queue
    )
    consumer.channel.basic_qos(prefetch_count=1)
    consumer.channel.basic_consume(queue=consumer.queue, on_message_callback=callback)
    logger.info('=========================Start consuming==================')
    logger.info(ConfigClass.gr_exchange)
    logger.info(ConfigClass.gr_queue)
    consumer.channel.start_consuming()


def instrument_app() -> None:
    """Instrument the application with OpenTelemetry tracing."""

    settings = get_settings()

    if not settings.OPEN_TELEMETRY_ENABLED:
        return

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: settings.APP_NAME}))
    trace.set_tracer_provider(tracer_provider)

    PikaInstrumentor().instrument()

    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.OPEN_TELEMETRY_HOST, agent_port=settings.OPEN_TELEMETRY_PORT
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))


def setup_logging(settings: ConfigClass) -> None:
    """Configure the application logging."""

    configure_logging(settings.LOGGING_LEVEL, settings.LOGGING_FORMAT)


if __name__ == '__main__':
    setup_logging(ConfigClass)
    instrument_app()
    main()
