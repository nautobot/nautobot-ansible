#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ip_address_to_interface
short_description: Creates or removes ip address to interface from Nautobot
description:
  - Creates or removes ip address to interface from Nautobot
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
  is_source:
    required: false
    type: bool
  is_destination:
    required: false
    type: bool
  is_default:
    required: false
    type: bool
  is_preferred:
    required: false
    type: bool
  is_primary:
    required: false
    type: bool
  is_secondary:
    required: false
    type: bool
  is_standby:
    required: false
    type: bool
  ip_address:
    required: true
    type: dict
  interface:
    required: false
    type: dict
  vm_interface:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create ip_address_to_interface within Nautobot with only required information
      networktocode.nautobot.ip_address_to_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        ip_address: None
        state: present

    - name: Delete ip_address_to_interface within nautobot
      networktocode.nautobot.ip_address_to_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
ip_address_to_interface:
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
    NB_IP_ADDRESS_TO_INTERFACE,
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
            is_source=dict(required=False, type="bool"),
            is_destination=dict(required=False, type="bool"),
            is_default=dict(required=False, type="bool"),
            is_preferred=dict(required=False, type="bool"),
            is_primary=dict(required=False, type="bool"),
            is_secondary=dict(required=False, type="bool"),
            is_standby=dict(required=False, type="bool"),
            ip_address=dict(required=True, type="dict"),
            interface=dict(required=False, type="dict"),
            vm_interface=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    ip_address_to_interface = NautobotIpamModule(module, NB_IP_ADDRESS_TO_INTERFACE)
    ip_address_to_interface.run()


if __name__ == "__main__":  # pragma: no cover
    main()
