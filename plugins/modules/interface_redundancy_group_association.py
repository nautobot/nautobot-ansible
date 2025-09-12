#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: interface_redundancy_group_association
short_description: Creates or removes interface redundancy group associations from Nautobot
description:
  - Creates or removes interface redundancy group associations from Nautobot
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
  priority:
    required: true
    type: int
  interface_redundancy_group:
    required: true
    type: dict
  interface:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create interface_redundancy_group_association within Nautobot with only required information
      networktocode.nautobot.interface_redundancy_group_association:
        url: http://nautobot.local
        token: thisIsMyToken
        priority: None
        interface_redundancy_group: None
        interface: None
        state: present

    - name: Delete interface_redundancy_group_association within nautobot
      networktocode.nautobot.interface_redundancy_group_association:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
interface_redundancy_group_association:
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
    NautobotDcimModule,
    NB_INTERFACE_REDUNDANCY_GROUP_ASSOCIATIONS,
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
            priority=dict(required=True, type="int"),
            interface_redundancy_group=dict(required=True, type="dict"),
            interface=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    interface_redundancy_group_association = NautobotDcimModule(module, NB_INTERFACE_REDUNDANCY_GROUP_ASSOCIATIONS)
    interface_redundancy_group_association.run()


if __name__ == "__main__":  # pragma: no cover
    main()
