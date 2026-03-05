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
from pipelines.copy_to_central_node import copy_to_central_node_pipeline
from pipelines.data_copy import folder_copy_pipeline
from pipelines.data_delete import folder_delete_pipeline
from pipelines.share_dataset_version import share_dataset_version_pipeline

from consumer import QueueConsumer


def millis():
    current_milli_time = str(round(time.time() * 1000))

    return current_milli_time


def bids_validator(ch, method, message):
    try:
        logger.info('bids_validate message has been received')
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


def share_dataset_version(ch, method, message):
    try:
        logger.info('share_dataset_version message has been received')
        version_id = message['version_id']
        destination_project_code = message['destination_project_code']
        job_id = message['job_id']
        session_id = message['session_id']
        operator = message['operator']
        access_token = message['access_token']
        try:
            share_dataset_version_pipeline(
                logger, version_id, destination_project_code, job_id, session_id, operator, access_token
            )
            logger.info('share_dataset_version pipeline is processing')
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.exception(f'Error occurred during share_dataset_version pipeline. {e}')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as e:
        logger.exception(f'Error occurred during share_dataset_version pipeline. {e}')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def copy_to_central_node(ch, method, message):
    try:
        logger.info('copy_to_central_node message has been received')
        job_id = message['job_id']
        session_id = message['session_id']
        file_id = message['file_id']
        destination_api_url = message['destination_api_url']
        destination_project_code = message['destination_project_code']
        destination_access_token = message['destination_access_token']
        operator = message['operator']
        access_token = message['access_token']
        try:
            copy_to_central_node_pipeline(
                logger,
                file_id,
                destination_api_url,
                destination_project_code,
                destination_access_token,
                job_id,
                session_id,
                operator,
                access_token,
            )
            logger.info('copy_to_central_node pipeline is processing')
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.exception(f'Error occurred during copy_to_central_node pipeline. {e}')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as e:
        logger.exception(f'Error occurred during copy_to_central_node pipeline. {e}')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def folder_copy(ch, method, message):
    try:
        logger.info('folder_copy message has been received')
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
        logger.info('folder_delete message has been received')
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

    logger.info(f'[x] Received {method} {body!r}')
    message = json.loads(body)

    name = method.routing_key.split('.')[-1]

    if name == 'bids_validate':
        bids_validator(ch, method, message)

    elif name == 'share_dataset_version':
        share_dataset_version(ch, method, message)

    elif name == 'copy_to_central_node':
        copy_to_central_node(ch, method, message)

    elif name == 'folder_copy':
        folder_copy(ch, method, message)

    elif name == 'folder_delete':
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
