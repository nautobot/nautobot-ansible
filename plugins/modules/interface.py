#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: interface
short_description: Creates or removes interfaces from Nautobot
description:
  - Creates or removes interfaces from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  mac_address:
    required: false
    type: str
  enabled:
    required: false
    type: bool
  mtu:
    required: false
    type: int
  mode:
    required: false
    type: str
    choices:
      - "access"
      - "tagged"
      - "tagged-all"
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  status:
    required: true
    type: str
  role:
    required: false
    type: dict
  parent_interface:
    required: false
    type: dict
  bridge:
    required: false
    type: dict
  virtual_machine:
    required: true
    type: dict
  untagged_vlan:
    required: false
    type: dict
  vrf:
    required: false
    type: dict
  tagged_vlans:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create interface within Nautobot with only required information
      networktocode.nautobot.interface:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface
        status: "Active"
        virtual_machine: None
        state: present

    - name: Delete interface within nautobot
      networktocode.nautobot.interface:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface
        state: absent
"""

RETURN = r"""
interface:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_INTERFACES,
    NautobotVirtualizationModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            mac_address=dict(required=False, type="str"),
            enabled=dict(required=False, type="bool"),
            mtu=dict(required=False, type="int"),
            mode=dict(
                required=False,
                type="str",
                choices=[
                    "access",
                    "tagged",
                    "tagged-all",
                ],
            ),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            status=dict(required=True, type="str"),
            role=dict(required=False, type="dict"),
            parent_interface=dict(required=False, type="dict"),
            bridge=dict(required=False, type="dict"),
            virtual_machine=dict(required=True, type="dict"),
            untagged_vlan=dict(required=False, type="dict"),
            vrf=dict(required=False, type="dict"),
            tagged_vlans=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    interface = NautobotVirtualizationModule(module, NB_INTERFACES)
    interface.run()


if __name__ == "__main__":  # pragma: no cover
    main()
