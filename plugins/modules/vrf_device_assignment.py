#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vrf_device_assignment
short_description: Creates or removes vrf device assignments from Nautobot
description:
  - Creates or removes vrf device assignments from Nautobot
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
  rd:
    required: false
    type: str
  name:
    required: false
    type: str
  vrf:
    required: true
    type: dict
  device:
    required: false
    type: dict
  virtual_machine:
    required: false
    type: dict
  virtual_device_context:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create vrf_device_assignment within Nautobot with only required information
      networktocode.nautobot.vrf_device_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        vrf: None
        state: present

    - name: Delete vrf_device_assignment within nautobot
      networktocode.nautobot.vrf_device_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
vrf_device_assignment:
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
    NautobotIpamModule,
    NB_VRF_DEVICE_ASSIGNMENTS,
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
            rd=dict(required=False, type="str"),
            name=dict(required=False, type="str"),
            vrf=dict(required=True, type="dict"),
            device=dict(required=False, type="dict"),
            virtual_machine=dict(required=False, type="dict"),
            virtual_device_context=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vrf_device_assignment = NautobotIpamModule(module, NB_VRF_DEVICE_ASSIGNMENTS)
    vrf_device_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
