#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: radio_profile
short_description: Manage radio profiles in Nautobot
description:
  - Manage radio profiles in Nautobot
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
      - The name of the radio profile
      - Required if I(state=present) and the radio profile does not exist yet
    required: false
    type: str
  regulatory_domain:
    description:
      - The regulatory domain of the radio profile
      - Required if I(state=present) and the radio profile does not exist yet
    required: false
    type: str
  channel_width:
    description:
      - The channel width of the radio profile
    required: false
    type: list
    elements: int
    choices:
      - 20
      - 40
      - 80
      - 160
  allowed_channel_list:
    description:
      - The allowed channel list of the radio profile
    required: false
    type: list
    elements: int
  frequency:
    description:
      - The frequency of the radio profile
    required: false
    type: str
    choices:
      - "2.4GHz"
      - "5GHz"
      - "6GHz"
  tx_power_min:
    description:
      - The minimum transmit power of the radio profile in dBm
    required: false
    type: int
  tx_power_max:
    description:
      - The maximum transmit power of the radio profile in dBm
    required: false
    type: int
  rx_power_min:
    description:
      - The minimum receive power of the radio profile in dBm
    required: false
    type: int
  supported_data_rates:
    description:
      - The supported data rates of the radio profile
    required: false
    type: list
    elements: raw
"""

EXAMPLES = r"""
---
- name: Create a radio profile with required fields
  networktocode.nautobot.radio_profile:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Radio Profile"
    regulatory_domain: "US"
    state: present

- name: Create a radio profile with all fields
  networktocode.nautobot.radio_profile:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Radio Profile"
    regulatory_domain: "US"
    channel_width: 20
    allowed_channel_list:
      - 1
      - 6
      - 11
    frequency: "2.4GHz"
    tx_power_min: 10
    tx_power_max: 20
    rx_power_min: 10
    supported_data_rates:
      - standard: "802.11a"
        rate: 1000000
        mcs_index: 10
    state: present

- name: Delete a radio profile
  networktocode.nautobot.radio_profile:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Radio Profile"
    state: absent

- name: Delete a radio profile by id
  networktocode.nautobot.radio_profile:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
radio_profile:
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
    NB_WIRELESS_RADIO_PROFILES,
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
            regulatory_domain=dict(required=False, type="str"),
            channel_width=dict(required=False, type="list", elements="int", choices=[20, 40, 80, 160]),
            allowed_channel_list=dict(required=False, type="list", elements="int"),
            frequency=dict(required=False, type="str", choices=["2.4GHz", "5GHz", "6GHz"]),
            tx_power_min=dict(required=False, type="int"),
            tx_power_max=dict(required=False, type="int"),
            rx_power_min=dict(required=False, type="int"),
            supported_data_rates=dict(required=False, type="list", elements="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    radio_profile = NautobotWirelessModule(module, NB_WIRELESS_RADIO_PROFILES)
    radio_profile.run()


if __name__ == "__main__":  # pragma: no cover
    main()
