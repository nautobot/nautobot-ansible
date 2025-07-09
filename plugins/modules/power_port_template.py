#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_port_template
short_description: Create, update or delete power port templates within Nautobot
description:
  - Creates, updates or removes power port templates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  device_type:
    description:
      - The device type the power port is attached to
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the power port
    required: true
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the power port
    required: false
    type: str
    version_added: "3.0.0"
  allocated_draw:
    description:
      - The allocated draw of the power port in watt
    required: false
    type: int
    version_added: "3.0.0"
  maximum_draw:
    description:
      - The maximum permissible draw of the power port in watt
    required: false
    type: int
    version_added: "3.0.0"
  module_type:
    description:
      - The module type the power port template is attached to
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
      networktocode.nautobot.power_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Port Template
        device_type: Test Device Type
        state: present

    - name: Update power port with other fields
      networktocode.nautobot.power_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Port Template
        device_type: Test Device Type
        type: iec-60320-c6
        allocated_draw: 16
        maximum_draw: 80
        state: present

    - name: Delete power port within nautobot
      networktocode.nautobot.power_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Port Template
        device_type: Test Device Type
        state: absent
"""

RETURN = r"""
power_port_template:
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
    NB_POWER_PORT_TEMPLATES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            device_type=dict(required=False, type="raw"),
            name=dict(required=True, type="str"),
            type=dict(required=False, type="str"),
            allocated_draw=dict(required=False, type="int"),
            maximum_draw=dict(required=False, type="int"),
            module_type=dict(required=False, type="raw"),
        )
    )

    required_one_of = [
        ("device_type", "module_type"),
    ]
    mutually_exclusive = [
        ("device_type", "module_type"),
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=required_one_of,
        mutually_exclusive=mutually_exclusive,
    )

    power_port_template = NautobotDcimModule(module, NB_POWER_PORT_TEMPLATES)
    power_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
