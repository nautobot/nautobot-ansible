#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

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
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  power_panel:
    description:
      - The power panel the power feed is terminated on
    required: true
    type: raw
  rack:
    description:
      - The rack the power feed is assigned to
    required: false
    type: raw
  name:
    description:
      - The name of the power feed
    required: true
    type: str
  status:
    description:
      - The status of the power feed
    required: false
    type: str
  type:
    description:
      - The type of the power feed
    choices:
      - primary
      - redundant
    required: false
    type: str
  supply:
    description:
      - The supply type of the power feed
    choices:
      - ac
      - dc
    required: false
    type: str
  phase:
    description:
      - The phase type of the power feed
    choices:
      - single-phase
      - three-phase
    required: false
    type: str
  voltage:
    description:
      - The voltage of the power feed
    required: false
    type: int
  amperage:
    description:
      - The amperage of the power feed
    required: false
    type: int
  max_utilization:
    description:
      - The maximum permissible draw of the power feed in percent
    required: false
    type: int
  comments:
    description:
      - Comments related to the power feed
    required: false
    type: str
  tags:
    description:
      - Any tags that the power feed may need to be associated with
    required: false
    type: list
    elements: raw
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
    type: dict
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
)
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
    argument_spec.update(
        dict(
            power_panel=dict(required=True, type="raw"),
            rack=dict(required=False, type="raw"),
            name=dict(required=True, type="str"),
            status=dict(required=False, type="str",),
            type=dict(required=False, choices=["primary", "redundant"], type="str"),
            supply=dict(required=False, choices=["ac", "dc"], type="str"),
            phase=dict(
                required=False, choices=["single-phase", "three-phase"], type="str",
            ),
            voltage=dict(required=False, type="int"),
            amperage=dict(required=False, type="int"),
            max_utilization=dict(required=False, type="int"),
            comments=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    required_if = [
        ("state", "present", ["power_panel", "name", "status"]),
        ("state", "absent", ["power_panel", "name"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    power_feed = NautobotDcimModule(module, NB_POWER_FEEDS)
    power_feed.run()


if __name__ == "__main__":  # pragma: no cover
    main()
