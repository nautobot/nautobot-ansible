"""
nautobot_changelog.py.

event-driven-ansible source plugin for Nautobot Changelog via /extras/object-changes/

Poll Nautobot API for new changelog records
Only retrieves logs created after the script began executing
This script can be tested outside of ansible-rulebook by specifying
environment variables for NAUTOBOT_HOST, NAUTOBOT_TOKEN

Arguments:
  - instance: Nautobot instance (e.g. https://demo.nautobot.com)
  - token: Nautobot API Token
  - query:    (optional) Logs to query. Defaults to Logs created today
  - interval: (optional) How often to poll for new changelogs. Defaults to 5 seconds

- name: Watch for new changelog entries
  hosts: localhost
  sources:
    - jeffkala.nautobot_eda.nautobot_changelog:
        instance: https://demo.nautobot.com)
        token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        interval: 1
  rules:
    - name: New changelog created
      condition: event.id is defined
      action:
        debug:
"""

import asyncio
import time
import os
from typing import Any, Dict
import aiohttp


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    """Entrypoint from ansible-rulebook."""
    instance = args.get("instance")  # pylint:disable=W0621
    token = args.get("token")  # pylint:disable=W0621
    query = args.get("query", "")
    interval = int(args.get("interval", 5))

    start_time = time.time()
    start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time))
    printed_records = set()
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        # "version": "1.5",
        "Accept": "application/json",
    }
    if query:
        url = f"{instance}/api/extras/object-changes/?={query}"
    else:
        url = f"{instance}/api/extras/object-changes/?depth=0"
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            async with session.get(url) as resp:
                if resp.status == 200:
                    records = await resp.json()
                    for record in records["results"]:
                        # "time": "2023-02-22T03:07:51.453470Z",
                        if record["time"] > start_time_str and record["id"] not in printed_records:
                            printed_records.add(record["id"])
                            await queue.put(record['object_data'])

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
