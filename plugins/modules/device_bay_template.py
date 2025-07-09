#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_bay_template
short_description: Create, update or delete device bay templates within Nautobot
description:
  - Creates, updates or removes device bay templates from Nautobot
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
      - The device type the device bay template will be associated to. The device type must be "parent".
    required: true
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the device bay template
    required: true
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create device bay template within Nautobot with only required information
      networktocode.nautobot.device_bay_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: device bay template One
        device_type: Device Type One
        state: present

    - name: Delete device bay template within nautobot
      networktocode.nautobot.device_bay_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: device bay template One
        device_type: Device Type One
        state: absent
"""

RETURN = r"""
device_bay_template:
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
    NB_DEVICE_BAY_TEMPLATES,
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
            device_type=dict(required=True, type="raw"),
            name=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_bay_template = NautobotDcimModule(module, NB_DEVICE_BAY_TEMPLATES)
    device_bay_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
