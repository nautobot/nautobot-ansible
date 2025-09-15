#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: permission
short_description: Creates or removes permissions from Nautobot
description:
  - Creates or removes permissions from Nautobot
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
  object_types:
    required: true
    type: list
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  enabled:
    required: false
    type: bool
  actions:
    required: true
    type: str
  constraints:
    required: false
    type: str
  groups:
    required: false
    type: list
  users:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create permission within Nautobot with only required information
      networktocode.nautobot.permission:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Permission
        object_types: None
        actions: None
        state: present

    - name: Delete permission within nautobot
      networktocode.nautobot.permission:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Permission
        state: absent
"""

RETURN = r"""
permission:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.users import (
    NB_PERMISSIONS,
    NautobotUsersModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            object_types=dict(required=True, type="list"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            enabled=dict(required=False, type="bool"),
            actions=dict(required=True, type="str"),
            constraints=dict(required=False, type="str"),
            groups=dict(required=False, type="list"),
            users=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    permission = NautobotUsersModule(module, NB_PERMISSIONS)
    permission.run()


if __name__ == "__main__":  # pragma: no cover
    main()
