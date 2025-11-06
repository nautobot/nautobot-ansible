import asyncio
import os
import time
from typing import Any, Dict

import aiohttp

DOCUMENTATION = r"""
---
short_description: Source plugin for Nautobot Changelog via Object-Changes.
description:
  - An event-driven-ansible source plugin for Nautobot Changelog
    via /extras/object-changes/.
    Poll Nautobot API for new changelog records
    Only retrieves logs created after the script began executing
    This script can be tested outside of ansible-rulebook by specifying
    environment variables for NAUTOBOT_HOST, NAUTOBOT_TOKEN.
options:
  instance:
    description:
      - Nautobot instance (e.g. https://demo.nautobot.com).
    type: str
    default: "http://localhost:8080"
  token:
    description:
      - Nautobot API Token.
    type: str
    default: "0123456789abcdef0123456789abcdef01234567"
  query:
    description:
      - Logs to query. Defaults to Logs created today.
    type: str
    default: "today"
  interval:
    description:
      - How often to poll for new changelogs. Defaults to 5 seconds.
    type: int
    default: "5"
  validate_certs:
    description:
      - Whether to verify SSL certificates.
    type: bool
    default: true
"""


EXAMPLES = r"""
- name: Watch for new changelog entries
  hosts: localhost
  sources:
    - nautobot_ansible.eda.nautobot_changelog:
        instance: https://demo.nautobot.com
        token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        interval: 1
  rules:
    - name: New changelog created
      condition: event.id is defined
      action:
        debug:
"""


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    """Entrypoint from ansible-rulebook."""
    instance = args.get("instance")  # pylint:disable=W0621
    token = args.get("token")  # pylint:disable=W0621
    ssl_verify = args.get("validate_certs", True)
    if not isinstance(ssl_verify, bool):
        raise TypeError(
            f"validate_certs must be a boolean, got {type(ssl_verify).__name__}"
        )
    query = args.get("query", "")
    interval = int(args.get("interval", 5))

    start_time = time.time()
    start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time))
    printed_records = set()
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if query:
        url = f"{instance}/api/extras/object-changes/?={query}"
    else:
        url = f"{instance}/api/extras/object-changes/?depth=0"
    connector = aiohttp.TCPConnector(ssl=ssl_verify)
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        while True:
            async with session.get(url) as resp:
                if resp.status == 200:
                    records = await resp.json()
                    for record in records["results"]:
                        # "time": "2023-02-22T03:07:51.453470Z",
                        if record["time"] > start_time_str and record["id"] not in printed_records:
                            printed_records.add(record["id"])
                            await queue.put(record["object_data"])

                else:
                    print(f"Error {resp.status}")
            await asyncio.sleep(interval)


# this is only called when testing plugin directly, without ansible-rulebook
if __name__ == "__main__":
    instance = os.environ.get("NAUTOBOT_HOST")
    token = os.environ.get("NAUTOBOT_TOKEN")

    class MockQueue:  # pylint:disable=too-few-public-methods
        """Simple Mock to be able to execute this program without ansible-rulebook."""

        print("Waiting for events in Nautobot ChangeLog...")

        async def put(self, event):
            """Put event into the Mock Queue."""
            print(event)

    asyncio.run(main(MockQueue(), {"instance": instance, "token": token}))
