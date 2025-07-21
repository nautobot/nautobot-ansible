#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_feed
short_description: Create, update or delete power feeds within Nautobot
description:
  - Creates, updates or removes power feeds from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  power_panel:
    description:
      - The power panel the power feed is terminated on
      - Required if I(state=present) and the power feed does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  rack:
    description:
      - The rack the power feed is assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the power feed
      - Required if I(state=present) and the power feed does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  status:
    description:
      - The status of the power feed
      - Required if I(state=present) and does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the power feed
    choices:
      - primary
      - redundant
    required: false
    type: str
    version_added: "3.0.0"
  supply:
    description:
      - The supply type of the power feed
    choices:
      - ac
      - dc
    required: false
    type: str
    version_added: "3.0.0"
  phase:
    description:
      - The phase type of the power feed
    choices:
      - single-phase
      - three-phase
    required: false
    type: str
    version_added: "3.0.0"
  voltage:
    description:
      - The voltage of the power feed
    required: false
    type: int
    version_added: "3.0.0"
  amperage:
    description:
      - The amperage of the power feed
    required: false
    type: int
    version_added: "3.0.0"
  max_utilization:
    description:
      - The maximum permissible draw of the power feed in percent
    required: false
    type: int
    version_added: "3.0.0"
  comments:
    description:
      - Comments related to the power feed
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create power feed within Nautobot with only required information
      networktocode.nautobot.power_feed:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Feed
        power_panel: Test Power Panel
        status: active
        state: present

    - name: Update power feed with other fields
      networktocode.nautobot.power_feed:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Feed
        power_panel: Test Power Panel
        status: offline
        type: primary
        supply: ac
        phase: single-phase
        voltage: 230
        amperage: 16
        max_utilization: 80
        comments: normal power feed
        state: present

    - name: Delete power feed within nautobot
      networktocode.nautobot.power_feed:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Feed
        power_panel: Test Power Panel
        state: absent

    - name: Delete power feed by id
      networktocode.nautobot.power_feed:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
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

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_POWER_FEEDS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
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
            power_panel=dict(required=False, type="raw"),
            rack=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            status=dict(
                required=False,
                type="str",
            ),
            type=dict(required=False, choices=["primary", "redundant"], type="str"),
            supply=dict(required=False, choices=["ac", "dc"], type="str"),
            phase=dict(
                required=False,
                choices=["single-phase", "three-phase"],
                type="str",
            ),
            voltage=dict(required=False, type="int"),
            amperage=dict(required=False, type="int"),
            max_utilization=dict(required=False, type="int"),
            comments=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_feed = NautobotDcimModule(module, NB_POWER_FEEDS)
    power_feed.run()


if __name__ == "__main__":  # pragma: no cover
    main()
