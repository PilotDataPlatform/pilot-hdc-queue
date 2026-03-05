# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import base64
import time

from config import ConfigClass
from job import KubernetesApiClient
from kubernetes.client.rest import ApiException


def copy_to_central_node_pipeline(
    logger,
    file_id: str,
    destination_api_url: str,
    destination_project_code: str,
    destination_access_token: str,
    job_id: str,
    session_id: str,
    operator: str,
    access_token: str,
):
    volume_path = ConfigClass.data_lake
    command = ['python3', '-m', 'operations', 'copy-to-central-node']
    args = [
        '--file-id',
        file_id,
        '--destination-api-url-base64',
        base64.urlsafe_b64encode(destination_api_url.encode()).decode(),
        '--destination-project-code',
        destination_project_code,
        '--destination-access-token',
        destination_access_token,
        '--job-id',
        job_id,
        '--session-id',
        session_id,
        '--operator',
        operator,
        '--access-token',
        access_token,
    ]
    try:
        api_client = KubernetesApiClient()
        job_api_client = api_client.create_batch_api_client()
        job = api_client.copy_to_central_node_job_obj(
            'copy-to-central-node-' + str(round(time.time() * 10000)),
            ConfigClass.data_transfer_image,
            volume_path,
            command,
            args,
            file_id,
            destination_api_url,
            destination_project_code,
        )

        api_response = job_api_client.create_namespaced_job(namespace=ConfigClass.namespace, body=job)
        logger.info(api_response.status)
        return api_response
    except ApiException as e:
        logger.exception(f'Copy to central node failed {e}')
        raise e
