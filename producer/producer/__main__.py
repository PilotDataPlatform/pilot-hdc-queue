# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import uvicorn

from producer.config import get_settings

if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run('producer.app:create_app', factory=True, host=settings.host, port=settings.port)
