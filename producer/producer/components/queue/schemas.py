# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from enum import Enum
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import root_validator

from producer.components.schemas import APIResponse
from producer.components.schemas import BasePayload
from producer.components.schemas import BaseSchema


class Event(Enum):
    bids_validate = 'bids_validate'
    folder_copy = 'folder_copy'
    folder_delete = 'folder_delete'


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
    generic: Optional[str]
    operator: str
    request_info: Optional[Dict]
    destination_geid: str
    access_token: str


class DeletePayload(BasePayload):
    session_id: str
    job_id: str
    source_geid: str
    include_geids: list
    project: str
    generic: Optional[str]
    operator: str
    access_token: str
