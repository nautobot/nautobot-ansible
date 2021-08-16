#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Benjamin Vergnaud (@bvergnaud)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

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
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  virtual_machine:
    description:
      - Name of the virtual machine the interface will be associated with (case-sensitive)
    required: true
    type: raw
  name:
    description:
      - Name of the interface to be created
    required: true
    type: str
  enabled:
    description:
      - Sets whether interface shows enabled or disabled
    required: false
    type: bool
  mtu:
    description:
      - The MTU of the interface
    required: false
    type: int
  mac_address:
    description:
      - The MAC address of the interface
    required: false
    type: str
  description:
    description:
      - The description of the interface
    required: false
    type: str
  mode:
    description:
      - The mode of the interface
    required: false
    type: raw
  untagged_vlan:
    description:
      - The untagged VLAN to be assigned to interface
    required: false
    type: raw
  tagged_vlans:
    description:
      - A list of tagged VLANS to be assigned to interface. Mode must be set to either C(Tagged) or C(Tagged All)
    required: false
    type: raw
  tags:
    description:
      - Any tags that the prefix may need to be associated with
    required: false
    type: list
    elements: raw
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot interface module"
  connection: local
  hosts: localhost
  gather_facts: False
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
          site: Test Site
        tagged_vlans:
          - name: Data
            site: Test Site
          - name: VoIP
            site: Test Site
        mtu: 1600
        mode: Tagged
        state: present
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
    argument_spec.update(
        dict(
            virtual_machine=dict(required=True, type="raw"),
            name=dict(required=True, type="str"),
            enabled=dict(required=False, type="bool"),
            mtu=dict(required=False, type="int"),
            mac_address=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            mode=dict(required=False, type="raw"),
            untagged_vlan=dict(required=False, type="raw"),
            tagged_vlans=dict(required=False, type="raw"),
            tags=dict(required=False, type="list", elements="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vm_interface = NautobotVirtualizationModule(module, NB_VM_INTERFACES)
    vm_interface.run()


if __name__ == "__main__":  # pragma: no cover
    main()
