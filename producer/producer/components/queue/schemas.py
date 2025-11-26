# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from enum import Enum

from pydantic import BaseModel
from pydantic import root_validator

from producer.components.schemas import APIResponse
from producer.components.schemas import BasePayload
from producer.components.schemas import BaseSchema


class Event(Enum):
    bids_validate = 'bids_validate'
    folder_copy = 'folder_copy'
    folder_delete = 'folder_delete'
    share_dataset_version = 'share_dataset_version'


class SendMessageRequestSchema(BaseSchema):
    """Publish broker request schema."""

    event_type: Event
    payload: dict
    create_timestamp: float

    @root_validator
    def validate(cls, value):
        event_map = {
            'bids_validate': BidsPayload,
            'folder_copy': CopyPayload,
            'folder_delete': DeletePayload,
            'share_dataset_version': ShareDatasetVersion,
        }.get(value['event_type'])
        try:
            event_map(**value['payload'])
            return value
        except Exception as e:
            raise ValueError(e)

    def to_dict(self):
        return self.dict()


class SendMessageResponseSchema(APIResponse):
    result: str = ''


class BidsPayload(BaseModel):
    dataset_code: str
    access_token: str


class CopyPayload(BasePayload):
    session_id: str
    job_id: str
    source_geid: str
    include_geids: list
    project: str
    generic: str | None
    operator: str
    request_info: dict | None
    destination_geid: str
    access_token: str


class DeletePayload(BasePayload):
    session_id: str
    job_id: str
    source_geid: str
    include_geids: list
    project: str
    generic: str | None
    operator: str
    access_token: str


class ShareDatasetVersion(BasePayload):
    version_id: str
    destination_project_code: str
    job_id: str
    session_id: str
    operator: str
    access_token: str
