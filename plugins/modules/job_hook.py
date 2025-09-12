#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: job_hook
short_description: Creates or removes job hooks from Nautobot
description:
  - Creates or removes job hooks from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  content_types:
    required: true
    type: list
  enabled:
    required: false
    type: bool
  name:
    required: true
    type: str
  type_create:
    required: false
    type: bool
  type_delete:
    required: false
    type: bool
  type_update:
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
    - name: Create job_hook within Nautobot with only required information
      networktocode.nautobot.job_hook:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Job_Hook
        content_types: None
        job: None
        state: present

    - name: Delete job_hook within nautobot
      networktocode.nautobot.job_hook:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Job_Hook
        state: absent
"""

RETURN = r"""
job_hook:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_JOB_HOOKS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            content_types=dict(required=True, type="list"),
            enabled=dict(required=False, type="bool"),
            name=dict(required=True, type="str"),
            type_create=dict(required=False, type="bool"),
            type_delete=dict(required=False, type="bool"),
            type_update=dict(required=False, type="bool"),
            job=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    job_hook = NautobotExtrasModule(module, NB_JOB_HOOKS)
    job_hook.run()


if __name__ == "__main__":  # pragma: no cover
    main()
