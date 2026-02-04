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
  - networktocode.nautobot.fragments.id
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

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    NautobotModule,
)

# Keys to remove from module params before processing
REMOVE_KEYS = ["job", "interval", "start_time", "crontab", "data", "task_queue"]


class NautobotScheduledJobModule(NautobotModule):
    """Nautobot module for scheduled jobs with non-standard CRUD operations.

    Scheduled jobs have unique API behavior:
    - Create: POST to /api/extras/jobs/{id}/run/ with schedule parameter
    - Read/Delete: /api/extras/scheduled-jobs/
    - Update: Not supported (must delete and recreate)
    """

    def __init__(self, module):
        """Initialize the scheduled job module."""
        # Initialize parent with scheduled_jobs endpoint
        # Pass remove_keys to exclude non-standard params from data building
        super().__init__(module, "scheduled_jobs", remove_keys=REMOVE_KEYS)

    def run(self):
        """Execute the scheduled job module logic."""
        self.result = {"changed": False}

        if self.state == "present":
            self._ensure_scheduled_job_present()
        else:
            self._ensure_scheduled_job_absent()

        self.module.exit_json(**self.result)

    def _find_job(self, job_identifier):
        """Find a job by name or UUID.

        Args:
            job_identifier: Job name, module_name, or UUID

        Returns:
            Job object from pynautobot

        Raises:
            Module failure if job not found
        """
        jobs_endpoint = self.nb.extras.jobs

        # Try UUID first if it looks like one
        if self.is_valid_uuid(job_identifier):
            job = self._nb_endpoint_get(jobs_endpoint, {"id": job_identifier}, job_identifier)
            if job:
                return job

        # Try by name
        job = self._nb_endpoint_get(jobs_endpoint, {"name": job_identifier}, job_identifier)
        if job:
            return job

        # Try by module_name (full path like "plugins/my_plugin.jobs/MyJob")
        job = self._nb_endpoint_get(jobs_endpoint, {"module_name": job_identifier}, job_identifier)
        if job:
            return job

        self._handle_errors(msg=f"Job '{job_identifier}' not found in Nautobot")

    def _find_scheduled_job(self, name=None, job_id=None):
        """Find an existing scheduled job by name or ID.

        Args:
            name: Scheduled job name
            job_id: Scheduled job UUID

        Returns:
            Scheduled job object or None if not found
        """
        scheduled_jobs = self.nb.extras.scheduled_jobs

        try:
            if job_id:
                return scheduled_jobs.get(id=job_id)
            if name:
                return scheduled_jobs.get(name=name)
        except Exception:
            pass

        return None

    def _ensure_scheduled_job_present(self):
        """Create a scheduled job if it doesn't exist."""
        job_identifier = self.module.params.get("job")
        name = self.module.params.get("name")
        interval = self.module.params.get("interval")
        start_time = self.module.params.get("start_time")
        crontab = self.module.params.get("crontab")
        data = self.module.params.get("data") or {}
        task_queue = self.module.params.get("task_queue")

        # Validate required parameters
        if not job_identifier:
            self._handle_errors(msg="'job' is required when state=present")
        if not name:
            self._handle_errors(msg="'name' is required when state=present")
        if not interval:
            self._handle_errors(msg="'interval' is required when state=present")

        # Validate interval-specific requirements
        if interval == "future" and not start_time:
            self._handle_errors(msg="'start_time' is required when interval=future")
        if interval == "custom" and not crontab:
            self._handle_errors(msg="'crontab' is required when interval=custom")

        # Check if scheduled job already exists
        existing = self._find_scheduled_job(name=name)
        if existing:
            self.result["scheduled_job"] = dict(existing)
            self.result["msg"] = f"Scheduled job '{name}' already exists"
            return

        if self.check_mode:
            self.result["changed"] = True
            self.result["msg"] = f"Scheduled job '{name}' would be created"
            self.result["diff"] = self._build_diff(
                before={"state": "absent"},
                after={"state": "present"}
            )
            return

        # Find the job to schedule
        job = self._find_job(job_identifier)

        # Build schedule payload
        schedule_data = {"name": name, "interval": interval}
        if start_time:
            schedule_data["start_time"] = start_time
        if crontab:
            schedule_data["crontab"] = crontab

        # Build run request payload
        run_kwargs = {"schedule": schedule_data}
        if data:
            run_kwargs["data"] = data
        if task_queue:
            run_kwargs["task_queue"] = task_queue

        # Create via job run endpoint
        try:
            result = self.nb.extras.jobs.run(job_id=str(job.id), **run_kwargs)

            # Extract scheduled job data from response
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
            self.result["diff"] = self._build_diff(
                before={"state": "absent"},
                after={"state": "present"}
            )

        except Exception as e:
            self._handle_errors(msg=f"Error creating scheduled job: {e}")

    def _ensure_scheduled_job_absent(self):
        """Delete a scheduled job if it exists."""
        name = self.module.params.get("name")
        job_id = self.module.params.get("id")

        if not name and not job_id:
            self._handle_errors(msg="Either 'name' or 'id' is required when state=absent")

        # Find the scheduled job
        scheduled_job = self._find_scheduled_job(name=name, job_id=job_id)
        identifier = job_id or name

        if not scheduled_job:
            self.result["msg"] = f"Scheduled job '{identifier}' already absent"
            return

        if self.check_mode:
            self.result["changed"] = True
            self.result["msg"] = f"Scheduled job '{scheduled_job.name}' would be deleted"
            self.result["diff"] = self._build_diff(
                before={"state": "present"},
                after={"state": "absent"}
            )
            return

        try:
            scheduled_job.delete()
            self.result["changed"] = True
            self.result["msg"] = f"Scheduled job '{scheduled_job.name}' deleted"
            self.result["diff"] = self._build_diff(
                before={"state": "present"},
                after={"state": "absent"}
            )

        except Exception as e:
            self._handle_errors(msg=f"Error deleting scheduled job: {e}")


def main():
    """Execute scheduled job module."""
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            job=dict(required=False, type="str"),
            name=dict(required=False, type="str"),
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
