#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_outlet_template
short_description: Create, update or delete power outlet templates within Nautobot
description:
  - Creates, updates or removes power outlet templates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  device_type:
    description:
      - The device type the power outlet is attached to
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the power outlet template does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the power outlet
      - Required if I(state=present) and the power outlet template does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the power outlet
    required: false
    type: str
    version_added: "3.0.0"
  power_port_template:
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
  module_type:
    description:
      - The module type the power outlet template is attached to
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the power outlet template does not exist yet
    required: false
    type: raw
    version_added: "5.4.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create power port within Nautobot with only required information
      networktocode.nautobot.power_outlet_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device_type: Test Device Type
        state: present

    - name: Update power port with other fields
      networktocode.nautobot.power_outlet_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device_type: Test Device Type
        type: iec-60320-c6
        power_port_template: Test Power Port
        feed_leg: A
        state: present

    - name: Delete power port within nautobot
      networktocode.nautobot.power_outlet_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device_type: Test Device Type
        state: absent

    - name: Delete power outlet template by id
      networktocode.nautobot.power_outlet_template:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
power_outlet_template:
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
    NB_POWER_OUTLET_TEMPLATES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            device_type=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            power_port_template=dict(required=False, type="raw"),
            feed_leg=dict(required=False, choices=["A", "B", "C"], type="str"),
            module_type=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_outlet_template = NautobotDcimModule(module, NB_POWER_OUTLET_TEMPLATES)
    power_outlet_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
