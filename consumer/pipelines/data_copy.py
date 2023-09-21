# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from config import ConfigClass
from job import KubernetesApiClient
from kubernetes.client.rest import ApiException


def folder_copy_pipeline(
    logger,
    source_id: str,
    destination_id: str,
    project_code: str,
    request_info: Optional[dict],
    include_ids: List[str],
    event_payload: Dict[str, Any],
    access_token: str,
):
    volume_path = ConfigClass.data_lake
    command = ['python3', '-m', 'operations', 'copy']
    args = [
        '--source-id',
        source_id,
        '--destination-id',
        destination_id,
        '--project-code',
        event_payload['project'],
        '--operator',
        event_payload['operator'],
        '--job-id',
        event_payload['job_id'],
        '--session-id',
        event_payload['session_id'],
        '--access-token',
        access_token,
    ]

    if request_info != {}:
        request_info_str = json.dumps(request_info)
        args.extend(['--request-info', request_info_str])

    if include_ids:
        args.extend(['--include-ids', ','.join(include_ids)])

    logger.info(f'Creating job using command {command} and args {args}')

    job_name = 'data-transfer-' + project_code + str(round(time.time() * 10000))

    try:
        api_client = KubernetesApiClient()
        job_api_client = api_client.create_batch_api_client()

        job = api_client.copy_folder_job_obj(
            job_name,
            ConfigClass.data_transfer_image,
            volume_path,
            command,
            args,
            project_code,
            event_payload,
        )

        api_response = job_api_client.create_namespaced_job(namespace=ConfigClass.namespace, body=job)
        logger.info(
            f'Job folder_copy with name "{job_name}" \
            has been submitted with status "{api_response.status}".'
        )
        return api_response
    except ApiException:
        logger.exception(
            f'An ApiException exception occurred while running folder_copy \
                pipeline with job name "{job_name}".'
        )
        raise
