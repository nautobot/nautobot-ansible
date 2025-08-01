#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: wireless_network
short_description: Manage wireless networks in Nautobot
description:
  - Manage wireless networks in Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.13.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the wireless network
      - Required if I(state=present) and the wireless network does not exist yet
    required: false
    type: str
  ssid:
    description:
      - The SSID of the wireless network
      - Required if I(state=present) and the wireless network does not exist yet
    required: false
    type: str
  mode:
    description:
      - The mode of the wireless network
      - Required if I(state=present) and the wireless network does not exist yet
    required: false
    type: str
    choices:
      - "Central"
      - "Fabric"
      - "Standalone (Autonomous)"
      - "Local (Flex)"
      - "Mesh"
      - "Bridge"
  authentication:
    description:
      - The authentication method of the wireless network
      - Required if I(state=present) and the wireless network does not exist yet
    required: false
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
  description:
    description:
      - The description of the wireless network
    required: false
    type: str
  enabled:
    description:
      - Whether the wireless network is enabled
    required: false
    type: bool
  hidden:
    description:
      - Whether the wireless network is hidden
    required: false
    type: bool
  secrets_group:
    description:
      - The secrets group of the wireless network
    required: false
    type: raw
  tenant:
    description:
      - The tenant of the wireless network
    required: false
    type: raw
"""

EXAMPLES = r"""
---
- name: Create a wireless network
  networktocode.nautobot.wireless_network:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Wireless Network"
    ssid: "C'mon in!"
    mode: "Central"
    authentication: "Open"
    state: present

- name: Create a wireless network with all options
  networktocode.nautobot.wireless_network:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Wireless Network"
    ssid: "My SSID"
    mode: "Central"
    description: "My Wireless Network Description"
    authentication: "WPA2 Personal"
    enabled: true
    hidden: false
    secrets_group: "My Secrets Group"
    tenant: "My Tenant"
    state: present

- name: Delete a wireless network
  networktocode.nautobot.wireless_network:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Wireless Network"
    state: absent

- name: Delete a wireless network by id
  networktocode.nautobot.wireless_network:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
wireless_network:
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
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.wireless import (
    NB_WIRELESS_NETWORKS,
    NautobotWirelessModule,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            ssid=dict(required=False, type="str"),
            mode=dict(
                required=False,
                type="str",
                choices=["Central", "Fabric", "Standalone (Autonomous)", "Local (Flex)", "Mesh", "Bridge"],
            ),
            authentication=dict(
                required=False,
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
            description=dict(required=False, type="str"),
            enabled=dict(required=False, type="bool"),
            hidden=dict(required=False, type="bool"),
            secrets_group=dict(required=False, type="raw", no_log=False),
            tenant=dict(required=False, type="raw"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    wireless_network = NautobotWirelessModule(module, NB_WIRELESS_NETWORKS)
    wireless_network.run()


if __name__ == "__main__":  # pragma: no cover
    main()
