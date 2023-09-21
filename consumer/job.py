# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from config import ConfigClass
from kubernetes import client
from kubernetes import config
from kubernetes.config import ConfigException


class KubernetesApiClient:
    """Init kubernetes job client and include create job function."""

    def __init__(self):
        try:
            config.load_incluster_config()
        except ConfigException:
            config.load_kube_config()
        self.configuration = client.Configuration()

    def create_batch_api_client(self):
        return client.BatchV1Api(client.ApiClient(self.configuration))

    def create_job(self, job_name, container_image, volume_path, command, args, pipeline, anno):
        """Define the persistent volume claim and mount pvc to k8s job container."""

        pvc = client.V1PersistentVolumeClaimVolumeSource(claim_name=ConfigClass.claim_name, read_only=False)
        volume = client.V1Volume(persistent_volume_claim=pvc, name=ConfigClass.NFS_MOUNT)
        volume_mount = client.V1VolumeMount(mount_path=volume_path, name=ConfigClass.NFS_MOUNT)

        env = [
            client.V1EnvVar(name='CONFIG_CENTER_ENABLED', value=str(ConfigClass.CONFIG_CENTER_ENABLED)),
            client.V1EnvVar(name='VAULT_URL', value=ConfigClass.VAULT_URL),
            client.V1EnvVar(name='VAULT_CRT', value=ConfigClass.VAULT_CRT),
            client.V1EnvVar(name='VAULT_TOKEN', value=ConfigClass.VAULT_TOKEN),
            client.V1EnvVar(name='GREEN_ZONE_LABEL', value=ConfigClass.GREEN_ZONE_LABEL),
            client.V1EnvVar(name='CORE_ZONE_LABEL', value=ConfigClass.CORE_ZONE_LABEL),
            client.V1EnvVar(name='RDS_DBNAME', value=ConfigClass.RDS_DBNAME),
            client.V1EnvVar(name='RDS_HOST', value=ConfigClass.RDS_HOST),
            client.V1EnvVar(name='RDS_PORT', value=ConfigClass.RDS_PORT),
            client.V1EnvVar(name='S3_HOST', value=ConfigClass.S3_HOST),
            client.V1EnvVar(name='S3_PORT', value=ConfigClass.S3_PORT),
            client.V1EnvVar(name='S3_INTERNAL_HTTPS', value=ConfigClass.S3_INTERNAL_HTTPS),
            client.V1EnvVar(name='DATAOPS_SERVICE', value=ConfigClass.DATAOPS_SERVICE),
            client.V1EnvVar(name='PROJECT_SERVICE', value=ConfigClass.PROJECT_SERVICE),
            client.V1EnvVar(name='KAFKA_URL', value=ConfigClass.KAFKA_URL),
            client.V1EnvVar(name='REDIS_HOST', value=ConfigClass.REDIS_HOST),
            client.V1EnvVar(name='REDIS_PORT', value=ConfigClass.REDIS_PORT),
            client.V1EnvVar(name='ATLAS_HOST', value=ConfigClass.ATLAS_HOST),
            client.V1EnvVar(name='ATLAS_PORT', value=ConfigClass.ATLAS_PORT),
            client.V1EnvVar(name='APPROVAL_SERVICE', value=ConfigClass.APPROVAL_SERVICE),
            client.V1EnvVar(name='NOTIFICATION_SERVICE', value=ConfigClass.NOTIFICATION_SERVICE),
            client.V1EnvVar(name='DATASET_SERVICE', value=ConfigClass.DATASET_SERVICE),
        ]

        container = client.V1Container(
            name=job_name,
            image=container_image,
            command=command,
            args=args,
            env=env,
            volume_mounts=[volume_mount],
            image_pull_policy='Always',
        )

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={'pipeline': pipeline}, annotations=anno),
            spec=client.V1PodSpec(
                restart_policy='Never',
                containers=[container],
                volumes=[volume],
            ),
        )

        spec = client.V1JobSpec(template=template, backoff_limit=0, completions=1, ttl_seconds_after_finished=60)
        job = client.V1Job(api_version='batch/v1', kind='Job', metadata=client.V1ObjectMeta(name=job_name), spec=spec)

        return job

    def bids_validate_job_obj(self, job_name, container_image, volume_path, command, args, dataset_code):
        anno = {'dataset': dataset_code}

        job = self.create_job(
            job_name, container_image, volume_path, command, args, ConfigClass.bids_validate_pipeline, anno
        )

        return job

    def copy_folder_job_obj(self, job_name, container_image, volume_path, command, args, project_code, event_payload):
        anno = {
            'source_geid': args[1],
            'destination_geid': args[3],
            'project': project_code,
        }
        for key in event_payload:
            anno['event_payload_' + key] = str(event_payload[key])

        job = self.create_job(
            job_name, container_image, volume_path, command, args, ConfigClass.copy_pipeline_folder, anno
        )

        return job

    def move_folder_job_obj(self, job_name, container_image, volume_path, command, args, project_code, event_payload):
        anno = {
            'source_geid': args[1],
            'project': project_code,
        }
        for key in event_payload:
            anno['event_payload_' + key] = str(event_payload[key])

        job = self.create_job(
            job_name, container_image, volume_path, command, args, ConfigClass.move_pipeline_folder, anno
        )

        return job
