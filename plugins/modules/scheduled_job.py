#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scheduled_job
short_description: Schedule or delete scheduled jobs in Nautobot
description:
  - Schedule jobs to run at a specific time or interval in Nautobot
  - Delete existing scheduled jobs from Nautobot
  - Note that scheduled jobs cannot be updated once created - to change a scheduled job,
    delete it and create a new one
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
  - The job must be enabled and cannot have C(has_sensitive_variables=True) to be scheduled
  - Scheduled jobs use different API endpoints for creation vs retrieval/deletion
author:
  - Network to Code (@networktocode)
requirements:
  - pynautobot
version_added: "5.6.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  job:
    description:
      - The job to schedule, specified by name or UUID
      - Required when I(state=present)
    required: false
    type: str
  name:
    description:
      - The name for this scheduled job instance
      - Required when I(state=present)
      - Used to identify the scheduled job for deletion when I(state=absent)
    required: false
    type: str
  id:
    description:
      - The UUID of the scheduled job
      - Can be used to delete a specific scheduled job when I(state=absent)
    required: false
    type: str
  interval:
    description:
      - The scheduling interval type
      - C(immediately) - Run the job immediately (not actually scheduled)
      - C(future) - Run once at a specific time in the future
      - C(hourly) - Run every hour
      - C(daily) - Run every day
      - C(weekly) - Run every week
      - C(custom) - Use a custom crontab expression
    required: false
    type: str
    choices:
      - immediately
      - future
      - hourly
      - daily
      - weekly
      - custom
  start_time:
    description:
      - The time to start running the job (ISO 8601 format)
      - Required for I(interval=future) and recommended for recurring intervals
      - "Example: 2030-01-01T01:00:00.000Z"
    required: false
    type: str
  crontab:
    description:
      - A crontab expression for custom scheduling
      - Required when I(interval=custom)
      - "Example: */15 * * * * (every 15 minutes)"
    required: false
    type: str
  data:
    description:
      - Input data to pass to the job
      - The structure depends on the specific job's required inputs
    required: false
    type: dict
    default: {}
  task_queue:
    description:
      - The task queue to run the job in
      - If not specified, the default queue will be used
    required: false
    type: str
"""

EXAMPLES = r"""
- name: Schedule a job to run immediately
  networktocode.nautobot.scheduled_job:
    url: http://nautobot.local
    token: thisIsMyToken
    job: "MyJobClass"
    name: "Immediate Job Run"
    interval: immediately
    state: present

- name: Schedule a job to run at a specific future time
  networktocode.nautobot.scheduled_job:
    url: http://nautobot.local
    token: thisIsMyToken
    job: "plugins/my_plugin.jobs/MyJob"
    name: "Future Job Run"
    interval: future
    start_time: "2030-01-01T01:00:00.000Z"
    state: present

- name: Schedule a job to run daily
  networktocode.nautobot.scheduled_job:
    url: http://nautobot.local
    token: thisIsMyToken
    job: "MyJobClass"
    name: "Daily Backup Job"
    interval: daily
    start_time: "2025-01-01T02:00:00.000Z"
    state: present

- name: Schedule a job with custom crontab (every 15 minutes)
  networktocode.nautobot.scheduled_job:
    url: http://nautobot.local
    token: thisIsMyToken
    job: "MyJobClass"
    name: "Custom Interval Job"
    interval: custom
    crontab: "*/15 * * * *"
    state: present

- name: Schedule a job with input data
  networktocode.nautobot.scheduled_job:
    url: http://nautobot.local
    token: thisIsMyToken
    job: "MyJobClass"
    name: "Job With Data"
    interval: immediately
    data:
      device_name: "router01"
      dry_run: true
    state: present

- name: Delete a scheduled job by name
  networktocode.nautobot.scheduled_job:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "Daily Backup Job"
    state: absent

- name: Delete a scheduled job by ID
  networktocode.nautobot.scheduled_job:
    url: http://nautobot.local
    token: thisIsMyToken
    id: "00000000-0000-0000-0000-000000000000"
    state: absent
"""

RETURN = r"""
scheduled_job:
  description: Serialized object as created within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

import traceback
from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

PYNAUTOBOT_IMP_ERR = None
try:
    import pynautobot

    HAS_PYNAUTOBOT = True
except ImportError:
    PYNAUTOBOT_IMP_ERR = traceback.format_exc()
    HAS_PYNAUTOBOT = False

NAUTOBOT_ARG_SPEC = dict(
    url=dict(type="str", required=True),
    token=dict(type="str", required=True, no_log=True),
    state=dict(required=False, default="present", choices=["present", "absent"]),
    query_params=dict(required=False, type="list", elements="str"),
    validate_certs=dict(type="raw", default=True),
    api_version=dict(type="str", required=False),
)


def is_valid_uuid(value):
    """Check if a string is a valid UUID."""
    import re

    uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
    return bool(uuid_pattern.match(str(value)))


class NautobotScheduledJobModule:
    """Handle scheduled job operations in Nautobot."""

    def __init__(self, module):
        """Initialize the scheduled job module."""
        self.module = module
        self.state = module.params["state"]
        self.check_mode = module.check_mode
        self.result = {"changed": False}

        if not HAS_PYNAUTOBOT:
            module.fail_json(msg=missing_required_lib("pynautobot"), exception=PYNAUTOBOT_IMP_ERR)

        # Connect to Nautobot
        url = module.params["url"]
        token = module.params["token"]
        ssl_verify = module.params["validate_certs"]
        api_version = module.params["api_version"]

        try:
            self.nb = pynautobot.api(url, token=token, api_version=api_version, verify=ssl_verify)
        except Exception as e:
            module.fail_json(msg=f"Failed to connect to Nautobot: {str(e)}")

    def run(self):
        """Execute the module logic."""
        if self.state == "present":
            self._create_scheduled_job()
        else:
            self._delete_scheduled_job()

        self.module.exit_json(**self.result)

    def _find_job(self, job_identifier):
        """Find a job by name or UUID.

        Returns the job object or fails if not found.
        """
        try:
            jobs_endpoint = self.nb.extras.jobs

            # Try to find by UUID first if it looks like a UUID
            if is_valid_uuid(job_identifier):
                job = jobs_endpoint.get(id=job_identifier)
                if job:
                    return job

            # Try to find by name
            job = jobs_endpoint.get(name=job_identifier)
            if job:
                return job

            # Try module_name (full path like "plugins/my_plugin.jobs/MyJob")
            job = jobs_endpoint.get(module_name=job_identifier)
            if job:
                return job

            self.module.fail_json(msg=f"Job '{job_identifier}' not found in Nautobot")

        except pynautobot.RequestError as e:
            self.module.fail_json(msg=f"Error finding job: {e.error}")

    def _find_scheduled_job(self, name=None, job_id=None):
        """Find an existing scheduled job by name or ID.

        Returns the scheduled job object or None if not found.
        """
        try:
            scheduled_jobs = self.nb.extras.scheduled_jobs

            if job_id:
                return scheduled_jobs.get(id=job_id)

            if name:
                return scheduled_jobs.get(name=name)

            return None

        except pynautobot.RequestError:
            return None

    def _create_scheduled_job(self):
        """Create a new scheduled job."""
        job_identifier = self.module.params.get("job")
        name = self.module.params.get("name")
        interval = self.module.params.get("interval")
        start_time = self.module.params.get("start_time")
        crontab = self.module.params.get("crontab")
        data = self.module.params.get("data") or {}
        task_queue = self.module.params.get("task_queue")

        # Validate required parameters
        if not job_identifier:
            self.module.fail_json(msg="'job' is required when state=present")
        if not name:
            self.module.fail_json(msg="'name' is required when state=present")
        if not interval:
            self.module.fail_json(msg="'interval' is required when state=present")

        # Validate interval-specific requirements
        if interval == "future" and not start_time:
            self.module.fail_json(msg="'start_time' is required when interval=future")
        if interval == "custom" and not crontab:
            self.module.fail_json(msg="'crontab' is required when interval=custom")

        # Check if a scheduled job with this name already exists
        existing = self._find_scheduled_job(name=name)
        if existing:
            # Scheduled jobs can't be updated, so we just report it exists
            self.result["scheduled_job"] = dict(existing)
            self.result["msg"] = f"Scheduled job '{name}' already exists"
            return

        if self.check_mode:
            self.result["changed"] = True
            self.result["msg"] = f"Scheduled job '{name}' would be created"
            return

        # Find the job to schedule
        job = self._find_job(job_identifier)

        # Build the schedule payload
        schedule_data = {"name": name, "interval": interval}

        if start_time:
            schedule_data["start_time"] = start_time
        if crontab:
            schedule_data["crontab"] = crontab

        # Build the full request payload for the job run endpoint
        # The pynautobot job.run() method passes kwargs to POST body
        run_kwargs = {"schedule": schedule_data}

        if data:
            run_kwargs["data"] = data
        if task_queue:
            run_kwargs["task_queue"] = task_queue

        # Call the job's run endpoint with schedule parameter
        try:
            # Use pynautobot's jobs.run() with job_id and schedule params
            result = self.nb.extras.jobs.run(job_id=str(job.id), **run_kwargs)

            # Try to get the scheduled job that was created
            # The response from run() with schedule returns the scheduled job info
            scheduled_job_data = {}
            if hasattr(result, "scheduled_job") and result.scheduled_job:
                scheduled_job_data = dict(result.scheduled_job)
            elif hasattr(result, "serialize"):
                scheduled_job_data = result.serialize()
            else:
                scheduled_job_data = {"job_id": str(job.id), "name": name}

            self.result["changed"] = True
            self.result["scheduled_job"] = scheduled_job_data
            self.result["msg"] = f"Scheduled job '{name}' created"

        except pynautobot.RequestError as e:
            self.module.fail_json(msg=f"Error creating scheduled job: {e.error}")

    def _delete_scheduled_job(self):
        """Delete an existing scheduled job."""
        name = self.module.params.get("name")
        job_id = self.module.params.get("id")

        if not name and not job_id:
            self.module.fail_json(msg="Either 'name' or 'id' is required when state=absent")

        # Find the scheduled job
        scheduled_job = self._find_scheduled_job(name=name, job_id=job_id)

        if not scheduled_job:
            identifier = job_id or name
            self.result["msg"] = f"Scheduled job '{identifier}' not found, nothing to delete"
            return

        if self.check_mode:
            self.result["changed"] = True
            self.result["msg"] = f"Scheduled job '{scheduled_job.name}' would be deleted"
            return

        try:
            scheduled_job.delete()
            self.result["changed"] = True
            self.result["msg"] = f"Scheduled job '{scheduled_job.name}' deleted"

        except pynautobot.RequestError as e:
            self.module.fail_json(msg=f"Error deleting scheduled job: {e.error}")


def main():
    """Execute scheduled job module."""
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            job=dict(required=False, type="str"),
            name=dict(required=False, type="str"),
            id=dict(required=False, type="str"),
            interval=dict(
                required=False,
                type="str",
                choices=["immediately", "future", "hourly", "daily", "weekly", "custom"],
            ),
            start_time=dict(required=False, type="str"),
            crontab=dict(required=False, type="str"),
            data=dict(required=False, type="dict", default={}),
            task_queue=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    scheduled_job_module = NautobotScheduledJobModule(module)
    scheduled_job_module.run()


if __name__ == "__main__":  # pragma: no cover
    main()
