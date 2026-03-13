#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: controller_managed_device_group_wireless_network_assignment
short_description: Creates or removes controller managed device group wireless network assignments from Nautobot
description:
  - Creates or removes controller managed device group wireless network assignments from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network to Code (@networktocode)
requirements:
  - pynautobot
version_added: "6.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  controller_managed_device_group:
    description:
      - Controller managed device group to assign the wireless network to
    required: false
    type: raw
  wireless_network:
    description:
      - Wireless network to assign to the controller managed device group
    required: false
    type: raw
  vlan:
    description:
      - VLAN associated with this wireless network assignment
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: Create a controller managed device group wireless network assignment
  networktocode.nautobot.controller_managed_device_group_wireless_network_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    controller_managed_device_group: "My Device Group"
    wireless_network: "My Wireless Network"
    state: present

- name: Create a controller managed device group wireless network assignment with a VLAN
  networktocode.nautobot.controller_managed_device_group_wireless_network_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    controller_managed_device_group: "My Device Group"
    wireless_network: "My Wireless Network"
    vlan: "My VLAN"
    state: present

- name: Delete a controller managed device group wireless network assignment
  networktocode.nautobot.controller_managed_device_group_wireless_network_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    controller_managed_device_group: "My Device Group"
    wireless_network: "My Wireless Network"
    state: absent

- name: Delete a controller managed device group wireless network assignment by id
  networktocode.nautobot.controller_managed_device_group_wireless_network_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
controller_managed_device_group_wireless_network_assignment:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.wireless import (
    NB_CONTROLLER_MANAGED_DEVICE_GROUP_WIRELESS_NETWORK_ASSIGNMENTS,
    NautobotWirelessModule,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            controller_managed_device_group=dict(required=False, type="raw"),
            wireless_network=dict(required=False, type="raw"),
            vlan=dict(required=False, type="raw"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    controller_managed_device_group_wireless_network_assignment = NautobotWirelessModule(
        module, NB_CONTROLLER_MANAGED_DEVICE_GROUP_WIRELESS_NETWORK_ASSIGNMENTS
    )
    controller_managed_device_group_wireless_network_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
