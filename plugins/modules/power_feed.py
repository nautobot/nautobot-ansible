#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_feed
short_description: Creates or removes power feeds from Nautobot
description:
  - Creates or removes power feeds from Nautobot
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
  type:
    required: false
    type: str
    choices:
      - "primary"
      - "redundant"
  supply:
    required: false
    type: str
    choices:
      - "ac"
      - "dc"
  phase:
    required: false
    type: str
    choices:
      - "single-phase"
      - "three-phase"
  voltage:
    required: false
    type: int
  amperage:
    required: false
    type: int
  max_utilization:
    required: false
    type: int
  comments:
    required: false
    type: str
  cable:
    required: false
    type: dict
  power_panel:
    required: true
    type: dict
  rack:
    required: false
    type: dict
  status:
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create power_feed within Nautobot with only required information
      networktocode.nautobot.power_feed:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power_Feed
        power_panel: None
        status: "Active"
        state: present

    - name: Delete power_feed within nautobot
      networktocode.nautobot.power_feed:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power_Feed
        state: absent
"""

RETURN = r"""
power_feed:
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
    NautobotDcimModule,
    NB_POWER_FEEDS,
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
            name=dict(required=True, type="str"),
            type=dict(
                required=False,
                type="str",
                choices=[
                    "primary",
                    "redundant",
                ],
            ),
            supply=dict(
                required=False,
                type="str",
                choices=[
                    "ac",
                    "dc",
                ],
            ),
            phase=dict(
                required=False,
                type="str",
                choices=[
                    "single-phase",
                    "three-phase",
                ],
            ),
            voltage=dict(required=False, type="int"),
            amperage=dict(required=False, type="int"),
            max_utilization=dict(required=False, type="int"),
            comments=dict(required=False, type="str"),
            cable=dict(required=False, type="dict"),
            power_panel=dict(required=True, type="dict"),
            rack=dict(required=False, type="dict"),
            status=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_feed = NautobotDcimModule(module, NB_POWER_FEEDS)
    power_feed.run()


if __name__ == "__main__":  # pragma: no cover
    main()
