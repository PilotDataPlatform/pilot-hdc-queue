# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from producer.components.queue.publisher import BasedProducer


def trigger_event(event_type, project, create_time, payload):
    client = BasedProducer(event_type, project, create_time, payload)
    res = client.publish()
    return res
