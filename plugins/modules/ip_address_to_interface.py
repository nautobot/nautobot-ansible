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
  - networktocode.nautobot.fragments.id
options:
  ip_address:
    description:
      - IP address to associate with an interface.
      - Required if I(state=present) and the IP address to interface association does not exist yet
    required: false
    type: raw
    version_added: "5.0.0"
  interface:
    description:
      - Device interface to associate with an IP.
      - Requires one of I(interface) or I(vm_interface) when I(state=present) and the IP address to interface association does not exist yet
    required: false
    type: raw
    version_added: "5.0.0"
  vm_interface:
    description:
      - VM interface to associate with an IP.
      - Requires one of I(interface) or I(vm_interface) when I(state=present) and the IP address to interface association does not exist yet
    required: false
    type: raw
    version_added: "5.0.0"
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

    - name: Delete IP address to interface association by id
      networktocode.nautobot.ip_address_to_interface:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        id: 00000000-0000-0000-0000-000000000000
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

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NB_IP_ADDRESS_TO_INTERFACE,
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
            ip_address=dict(required=False, type="raw"),
            interface=dict(required=False, type="raw"),
            vm_interface=dict(required=False, type="raw"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    ip_address = NautobotIpamModule(module, NB_IP_ADDRESS_TO_INTERFACE)
    ip_address.run()


if __name__ == "__main__":  # pragma: no cover
    main()
