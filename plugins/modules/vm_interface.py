#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Benjamin Vergnaud (@bvergnaud)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vm_interface
short_description: Creates or removes interfaces from virtual machines in Nautobot
description:
  - Creates or removes interfaces from virtual machines in Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Benjamin Vergnaud (@bvergnaud)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  virtual_machine:
    description:
      - Name of the virtual machine the interface will be associated with (case-sensitive)
    required: true
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - Name of the interface to be created
    required: true
    type: str
    version_added: "3.0.0"
  enabled:
    description:
      - Sets whether interface shows enabled or disabled
    required: false
    type: bool
    version_added: "3.0.0"
  mtu:
    description:
      - The MTU of the interface
    required: false
    type: int
    version_added: "3.0.0"
  mac_address:
    description:
      - The MAC address of the interface
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - The description of the interface
    required: false
    type: str
    version_added: "3.0.0"
  status:
    description:
      - The status of the interface.
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  mode:
    description:
      - The mode of the interface
    required: false
    type: raw
    version_added: "3.0.0"
  untagged_vlan:
    description:
      - The untagged VLAN to be assigned to interface
    required: false
    type: raw
    version_added: "3.0.0"
  tagged_vlans:
    description:
      - A list of tagged VLANS to be assigned to interface. Mode must be set to either C(Tagged) or C(Tagged All)
    required: false
    type: raw
    version_added: "3.0.0"
  role:
    description:
      - The role of the interface
    required: false
    type: raw
    version_added: "5.3.0"
  vrf:
    description:
      - The VRF assigned to the interface
    required: false
    type: raw
    version_added: "5.12.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot interface module"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create interface within Nautobot with only required information
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet1
        state: present

    - name: Delete interface within nautobot
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet1
        state: absent

    - name: Create interface as a trunk port
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet25
        enabled: false
        untagged_vlan:
          name: Wireless
          location: "{{ test_location['key'] }}"
        tagged_vlans:
          - name: Data
            location: "{{ test_location['key'] }}"
          - name: VoIP
            location: "{{ test_location['key'] }}"
        mtu: 1600
        role: Server
        mode: Tagged
        state: present

    - name: |
        Create an interface and update custom_field data point,
        setting the value to True
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet26
        enabled: false
        custom_fields:
          monitored: true
"""

RETURN = r"""
interface:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.virtualization import (
    NautobotVirtualizationModule,
    NB_VM_INTERFACES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            virtual_machine=dict(required=True, type="raw"),
            name=dict(required=True, type="str"),
            enabled=dict(required=False, type="bool"),
            mtu=dict(required=False, type="int"),
            mac_address=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            status=dict(required=False, type="raw"),
            mode=dict(required=False, type="raw"),
            untagged_vlan=dict(required=False, type="raw"),
            tagged_vlans=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            vrf=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vm_interface = NautobotVirtualizationModule(module, NB_VM_INTERFACES)
    vm_interface.run()


if __name__ == "__main__":  # pragma: no cover
    main()
