# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Optional

from pydantic import Field

from producer.components.schemas import APIResponse
from producer.components.schemas import BaseSchema


class PublishBrokerRequestSchema(BaseSchema):
    """Publish broker request schema."""

    queue: str
    routing_key: str
    event_type: str
    payload: dict = {}
    exchange: Optional[dict] = None
    create_timestamp: Optional[float] = None
    binary: Optional[bool] = False


class PublishBrokerResponseSchema(APIResponse):
    """Publish broker request schema."""

    result: dict = Field(
        {},
        example={
            'event_type': 'folder_copy',
            'payload': {},
            'create_timestamp': 1670356352.0888927,
        },
    )
