#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ip_address_to_interface
short_description: Creates or removes IP address to interface association from Nautobot
description:
  - Creates or removes IP address to interface association from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
  - Anthony Ruhier (@Anthony25)
  - Chris Tomkins (@ChrisTomkins25)
version_added: "5.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  ip_address:
    description:
      - IP address to associate with an interface.
    required: true
    type: raw
    version_added: "5.0.0"
  interface:
    description:
      - Device interface to associate with an IP.
    required: false
    type: raw
    version_added: "5.0.0"
  vm_interface:
    description:
      - VM interface to associate with an IP.
    required: false
    type: raw
    version_added: "5.0.0"
  state:
    description:
      - Use C(present) or C(absent) for adding, or removing.
    choices: [ absent, present ]
    default: present
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot IP address to interface module"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: "Add IP address on GigabitEthernet4 - test100"
      networktocode.nautobot.ip_address_to_interface:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        ip_address:
          address: "10.100.0.1/32"
          namespace: "Global"
        interface:
          name: GigabitEthernet4
          device: test100

    - name: "Delete IP address on GigabitEthernet4 - test100"
      networktocode.nautobot.ip_address_to_interface:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        ip_address:
          address: "10.100.0.1/32"
          namespace: "Global"
        interface:
          name: GigabitEthernet4
          device: test100
        state: absent

"""

RETURN = r"""
ip_address_to_interface:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
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
            ip_address=dict(required=True, type="raw"),
            interface=dict(required=False, type="raw"),
            vm_interface=dict(required=False, type="raw"),
        )
    )
    required_one_of = [
        ("interface", "vm_interface"),
    ]
    mutually_exclusive = [
        ("interface", "vm_interface"),
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=required_one_of,
        mutually_exclusive=mutually_exclusive,
    )

    ip_address = NautobotIpamModule(module, NB_IP_ADDRESS_TO_INTERFACE)
    ip_address.run()


if __name__ == "__main__":  # pragma: no cover
    main()
