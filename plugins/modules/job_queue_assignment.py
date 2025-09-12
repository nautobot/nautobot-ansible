#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: job_queue_assignment
short_description: Creates or removes job queue assignments from Nautobot
description:
  - Creates or removes job queue assignments from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  id:
    required: false
    type: str
  job:
    required: true
    type: dict
  job_queue:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create job_queue_assignment within Nautobot with only required information
      networktocode.nautobot.job_queue_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        job: None
        job_queue: None
        state: present

    - name: Delete job_queue_assignment within nautobot
      networktocode.nautobot.job_queue_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
job_queue_assignment:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NB_JOB_QUEUE_ASSIGNMENTS,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            job=dict(required=True, type="dict"),
            job_queue=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    job_queue_assignment = NautobotExtrasModule(module, NB_JOB_QUEUE_ASSIGNMENTS)
    job_queue_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
