# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
from enum import Enum

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class EAPIResponseCode(Enum):
    success = 200
    internal_error = 500
    bad_request = 400
    not_found = 404


class APIResponse(BaseModel):
    code: EAPIResponseCode = EAPIResponseCode.success
    error_msg: str = ''
    page: int = 0
    result = []

    def json_response(self):
        data = self.dict()
        data['code'] = self.code.value
        return JSONResponse(status_code=self.code.value, content=data)


class BaseSchema(BaseModel):
    """Base class for all available schemas."""

    def to_payload(self) -> dict[str, str]:
        return json.loads(self.json())


class BasePayload(BaseModel):
    """Base payload for queue producer."""

    pass
