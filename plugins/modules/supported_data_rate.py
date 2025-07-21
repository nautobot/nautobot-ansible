#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: supported_data_rate
short_description: Manage supported data rates in Nautobot
description:
  - Manage supported data rates in Nautobot
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
  standard:
    description:
      - The standard of the supported data rate
      - Required if I(state=present) and the supported data rate does not exist yet
    required: false
    type: str
    choices:
      - "802.11a"
      - "802.11b"
      - "802.11g"
      - "802.11n"
      - "802.11ac"
      - "802.11ax"
      - "802.11be"
  rate:
    description:
      - The rate in Kbps
      - Required if I(state=present) and the supported data rate does not exist yet
    required: false
    type: int
  mcs_index:
    description:
      - The Modulation and Coding Scheme (MCS) index is a value used in wireless communications to define the modulation type,
      - coding rate, and number of spatial streams used in a transmission.
    required: false
    type: int
"""

EXAMPLES = r"""
---
- name: Create a supported data rate
  networktocode.nautobot.supported_data_rate:
    url: http://nautobot.local
    token: thisIsMyToken
    standard: "802.11a"
    rate: 1000000
    state: present

- name: Delete a supported data rate
  networktocode.nautobot.supported_data_rate:
    url: http://nautobot.local
    token: thisIsMyToken
    standard: "802.11a"
    rate: 1000000
    state: absent

- name: Delete a supported data rate by id
  networktocode.nautobot.supported_data_rate:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
supported_data_rate:
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
    NB_WIRELESS_SUPPORTED_DATA_RATES,
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
            standard=dict(
                required=False,
                type="str",
                choices=["802.11a", "802.11b", "802.11g", "802.11n", "802.11ac", "802.11ax", "802.11be"],
            ),
            rate=dict(required=False, type="int"),
            mcs_index=dict(required=False, type="int"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    supported_data_rate = NautobotWirelessModule(module, NB_WIRELESS_SUPPORTED_DATA_RATES)
    supported_data_rate.run()


if __name__ == "__main__":  # pragma: no cover
    main()
