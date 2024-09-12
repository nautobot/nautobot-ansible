#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_outlet
short_description: Create, update or delete power outlets within Nautobot
description:
  - Creates, updates or removes power outlets from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
options:
  device:
    description:
      - The device the power outlet is attached to
    required: true
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the power outlet
    required: true
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the power outlet
    required: false
    type: str
    version_added: "3.0.0"
  power_port:
    description:
      - The attached power port
    required: false
    type: raw
    version_added: "3.0.0"
  feed_leg:
    description:
      - The phase, in case of three-phase feed
    choices:
      - A
      - B
      - C
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - Description of the power outlet
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create power port within Nautobot with only required information
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device: Test Device
        state: present

    - name: Update power port with other fields
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device: Test Device
        type: iec-60320-c6
        power_port: Test Power Port
        feed_leg: A
        description: power port description
        state: present

    - name: Delete power port within nautobot
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device: Test Device
        state: absent
"""

RETURN = r"""
power_outlet:
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
    TAGS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_POWER_OUTLETS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            device=dict(required=True, type="raw"),
            name=dict(required=True, type="str"),
            type=dict(required=False, type="str"),
            power_port=dict(required=False, type="raw"),
            feed_leg=dict(required=False, choices=["A", "B", "C"], type="str"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_outlet = NautobotDcimModule(module, NB_POWER_OUTLETS)
    power_outlet.run()


if __name__ == "__main__":  # pragma: no cover
    main()
