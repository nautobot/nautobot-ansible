#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vrf_device_assignment
short_description: Creates or removes VRF to device assignments in Nautobot
description:
  - Creates or removes VRF to device assignments in Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.14.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  vrf:
    description:
      - VRF to assign to the device or virtual machine
      - Required if I(state=present) and the VRF to device assignment does not exist yet
    required: false
    type: raw
  device:
    description:
      - Device to assign the VRF to
      - Requires one of I(device), I(virtual_machine), or I(virtual_device_context) if I(state=present) and the VRF to device assignment does not exist yet
    required: false
    type: raw
  virtual_machine:
    description:
      - Virtual machine to assign the VRF to
      - Requires one of I(device), I(virtual_machine), or I(virtual_device_context) if I(state=present) and the VRF to device assignment does not exist yet
    required: false
    type: raw
  virtual_device_context:
    description:
      - Virtual device context to assign the VRF to
      - Requires one of I(device), I(virtual_machine), or I(virtual_device_context) if I(state=present) and the VRF to device assignment does not exist yet
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: "Create a VRF to device assignment"
  networktocode.nautobot.vrf_device_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    vrf: "My VRF"
    device: "My Device"
    state: present

- name: "Create a VRF to virtual machine assignment"
  networktocode.nautobot.vrf_device_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    vrf: "My VRF"
    virtual_machine: "My Virtual Machine"
    state: present

- name: "Delete a VRF to device assignment"
  networktocode.nautobot.vrf_device_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    vrf: "My VRF"
    device: "My Device"
    state: absent

- name: "Delete a VRF to virtual machine assignment"
  networktocode.nautobot.vrf_device_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    vrf: "My VRF"
    virtual_machine: "My Virtual Machine"
    state: absent

- name: "Delete a VRF to device assignment by id"
  networktocode.nautobot.vrf_device_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
vrf_device_assignment:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating successful operation
  returned: success
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NB_VRF_DEVICE_ASSIGNMENTS,
    NautobotIpamModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            vrf=dict(required=False, type="raw"),
            device=dict(required=False, type="raw"),
            virtual_machine=dict(required=False, type="raw"),
            virtual_device_context=dict(required=False, type="raw"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    vrf_device_assignment = NautobotIpamModule(module, NB_VRF_DEVICE_ASSIGNMENTS)
    vrf_device_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
