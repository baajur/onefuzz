#!/usr/bin/env python
#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import logging
from typing import Dict

import azure.functions as func

from ..onefuzzlib.azure.storage import corpus_accounts
from ..onefuzzlib.events import get_events
from ..onefuzzlib.notifications.main import new_files


def file_added(event: Dict) -> None:
    parts = event["data"]["url"].split("/")[3:]
    container = parts[0]
    path = "/".join(parts[1:])
    logging.info("file added container: %s - path: %s", container, path)
    new_files(container, path)


def main(msg: func.QueueMessage, dashboard: func.Out[str]) -> None:
    event = json.loads(msg.get_body())

    if event["topic"] not in corpus_accounts():
        return

    if event["eventType"] != "Microsoft.Storage.BlobCreated":
        return

    file_added(event)

    events = get_events()
    if events:
        dashboard.set(events)
