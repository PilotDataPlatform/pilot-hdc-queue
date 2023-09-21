# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import time

from config import ConfigClass
from job import KubernetesApiClient
from kubernetes.client.rest import ApiException


def bids_validate_pipeline(logger, dataset_code, access_token):
    logger.info(f'The vault url is: {ConfigClass.VAULT_URL}')
    volume_path = ConfigClass.data_lake
    command = ['poetry', 'run', 'python', 'scripts/validate_dataset.py']
    args = [
        '-d',
        dataset_code,
        '-env',
        ConfigClass.env,
        '--access-token',
        access_token,
    ]
    try:
        api_client = KubernetesApiClient()
        job_api_client = api_client.create_batch_api_client()
        job = api_client.bids_validate_job_obj(
            'bids-validate-' + str(round(time.time() * 10000)),
            ConfigClass.bids_validate_image,
            volume_path,
            command,
            args,
            dataset_code,
        )

        api_response = job_api_client.create_namespaced_job(namespace=ConfigClass.namespace, body=job)
        logger.info(api_response.status)
        return api_response
    except ApiException as e:
        logger.exception(f'Bids validate failed {e}')
        return
