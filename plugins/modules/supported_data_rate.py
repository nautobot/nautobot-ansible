#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: supported_data_rate
short_description: Creates or removes supported data rates from Nautobot
description:
  - Creates or removes supported data rates from Nautobot
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
  standard:
    required: true
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
    required: true
    type: int
  mcs_index:
    required: false
    type: int
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create supported_data_rate within Nautobot with only required information
      networktocode.nautobot.supported_data_rate:
        url: http://nautobot.local
        token: thisIsMyToken
        standard: 802.11a
        rate: None
        state: present

    - name: Delete supported_data_rate within nautobot
      networktocode.nautobot.supported_data_rate:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
supported_data_rate:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotWirelessModule,
    NB_SUPPORTED_DATA_RATES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            standard=dict(
                required=True,
                type="str",
                choices=[
                    "802.11a",
                    "802.11b",
                    "802.11g",
                    "802.11n",
                    "802.11ac",
                    "802.11ax",
                    "802.11be",
                ],
            ),
            rate=dict(required=True, type="int"),
            mcs_index=dict(required=False, type="int"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    supported_data_rate = NautobotWirelessModule(module, NB_SUPPORTED_DATA_RATES)
    supported_data_rate.run()


if __name__ == "__main__":  # pragma: no cover
    main()
