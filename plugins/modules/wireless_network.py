#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: wireless_network
short_description: Creates or removes wireless networks from Nautobot
description:
  - Creates or removes wireless networks from Nautobot
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
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  ssid:
    required: true
    type: str
  mode:
    required: true
    type: str
    choices:
      - "Central"
      - "Fabric"
      - "Standalone (Autonomous)"
      - "Local (Flex)"
      - "Mesh"
      - "Bridge"
  enabled:
    required: false
    type: bool
  authentication:
    required: true
    type: str
    choices:
      - "Open"
      - "WPA2 Personal"
      - "WPA2 Enterprise"
      - "Enhanced Open"
      - "WPA3 Personal"
      - "WPA3 SAE"
      - "WPA3 Enterprise"
      - "WPA3 Enterprise 192Bit"
  hidden:
    required: false
    type: bool
  secrets_group:
    required: false
    type: dict
  tenant:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create wireless network within Nautobot with only required information
      networktocode.nautobot.wireless_network:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Wireless Network
        ssid: "Test ssid"
        mode: Central
        authentication: Open
        state: present

    - name: Delete wireless_network within nautobot
      networktocode.nautobot.wireless_network:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Wireless_Network
        state: absent
"""

RETURN = r"""
wireless_network:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.wireless import (
    NB_WIRELESS_NETWORKS,
    NautobotWirelessModule,
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
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            ssid=dict(required=True, type="str"),
            mode=dict(
                required=True,
                type="str",
                choices=[
                    "Central",
                    "Fabric",
                    "Standalone (Autonomous)",
                    "Local (Flex)",
                    "Mesh",
                    "Bridge",
                ],
            ),
            enabled=dict(required=False, type="bool"),
            authentication=dict(
                required=True,
                type="str",
                choices=[
                    "Open",
                    "WPA2 Personal",
                    "WPA2 Enterprise",
                    "Enhanced Open",
                    "WPA3 Personal",
                    "WPA3 SAE",
                    "WPA3 Enterprise",
                    "WPA3 Enterprise 192Bit",
                ],
            ),
            hidden=dict(required=False, type="bool"),
            secrets_group=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    wireless_network = NautobotWirelessModule(module, NB_WIRELESS_NETWORKS)
    wireless_network.run()


if __name__ == "__main__":  # pragma: no cover
    main()
