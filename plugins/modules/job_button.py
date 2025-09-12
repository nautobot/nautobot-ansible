#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: job_button
short_description: Creates or removes job buttons from Nautobot
description:
  - Creates or removes job buttons from Nautobot
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
  content_types:
    required: true
    type: list
  name:
    required: true
    type: str
  enabled:
    required: false
    type: bool
  text:
    required: true
    type: str
  weight:
    required: false
    type: int
  group_name:
    required: false
    type: str
  button_class:
    required: false
    type: str
    choices:
      - "default"
      - "primary"
      - "success"
      - "info"
      - "warning"
      - "danger"
      - "link"
  confirmation:
    required: false
    type: bool
  job:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create job_button within Nautobot with only required information
      networktocode.nautobot.job_button:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Job_Button
        content_types: None
        text: "Test text"
        job: None
        state: present

    - name: Delete job_button within nautobot
      networktocode.nautobot.job_button:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Job_Button
        state: absent
"""

RETURN = r"""
job_button:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_JOB_BUTTONS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            content_types=dict(required=True, type="list"),
            name=dict(required=True, type="str"),
            enabled=dict(required=False, type="bool"),
            text=dict(required=True, type="str"),
            weight=dict(required=False, type="int"),
            group_name=dict(required=False, type="str"),
            button_class=dict(
                required=False,
                type="str",
                choices=[
                    "default",
                    "primary",
                    "success",
                    "info",
                    "warning",
                    "danger",
                    "link",
                ],
            ),
            confirmation=dict(required=False, type="bool"),
            job=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    job_button = NautobotExtrasModule(module, NB_JOB_BUTTONS)
    job_button.run()


if __name__ == "__main__":  # pragma: no cover
    main()
