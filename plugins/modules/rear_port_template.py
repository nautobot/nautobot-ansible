#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rear_port_template
short_description: Create, update or delete rear port templates within Nautobot
description:
  - Creates, updates or removes rear port templates from Nautobot
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
      - The device type the rear port template is attached to
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the rear port template
    required: true
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the rear port
    required: true
    type: str
    version_added: "3.0.0"
  positions:
    description:
      - The number of front ports which may be mapped to each rear port
    required: false
    type: int
    version_added: "3.0.0"
  module_type:
    description:
      - The module type the rear port template is attached to
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
    - name: Create rear port template within Nautobot with only required information
      networktocode.nautobot.rear_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port Template
        device_type: Test Device Type
        type: bnc
        state: present

    - name: Update rear port template with other fields
      networktocode.nautobot.rear_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port Template
        device_type: Test Device Type
        type: bnc
        positions: 5
        state: present

    - name: Delete rear port template within nautobot
      networktocode.nautobot.rear_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port Template
        device_type: Test Device Type
        type: bnc
        state: absent
"""

RETURN = r"""
rear_port_template:
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
    NB_REAR_PORT_TEMPLATES,
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
            type=dict(required=True, type="str"),
            positions=dict(required=False, type="int"),
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

    rear_port_template = NautobotDcimModule(module, NB_REAR_PORT_TEMPLATES)
    rear_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
