# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import time

from config import ConfigClass
from job import KubernetesApiClient
from kubernetes.client.rest import ApiException


def share_dataset_version_pipeline(
    logger,
    version_id: str,
    destination_project_code: str,
    job_id: str,
    session_id: str,
    operator: str,
    access_token: str,
):
    volume_path = ConfigClass.data_lake
    command = ['python3', '-m', 'operations', 'share-dataset-version']
    args = [
        '--version-id',
        version_id,
        '--destination-project-code',
        destination_project_code,
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
        job = api_client.share_dataset_version_job_obj(
            'share-dataset-version-' + str(round(time.time() * 10000)),
            ConfigClass.data_transfer_image,
            volume_path,
            command,
            args,
            version_id,
            destination_project_code,
        )

        api_response = job_api_client.create_namespaced_job(namespace=ConfigClass.namespace, body=job)
        logger.info(api_response.status)
        return api_response
    except ApiException as e:
        logger.exception(f'Share dataset version failed {e}')
        return
