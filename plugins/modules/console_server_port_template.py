#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: console_server_port_template
short_description: Create, update or delete console server port templates within Nautobot
description:
  - Creates, updates or removes console server port templates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.custom_fields
options:
  device_type:
    description:
      - The device type the console server port template is attached to
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the console server port template does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the console server port template
      - Required if I(state=present) and the console server port template does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the console server port template
    required: false
    type: str
    version_added: "3.0.0"
  module_type:
    description:
      - The module type the console server port template is attached to
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the console server port template does not exist yet
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
    - name: Create console server port template within Nautobot with only required information
      networktocode.nautobot.console_server_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console Server Port Template
        device_type: Test Device Type
        state: present

    - name: Update console server port template with other fields
      networktocode.nautobot.console_server_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console Server Port Template
        device_type: Test Device Type
        type: iec-60320-c6
        state: present

    - name: Delete console server port template within nautobot
      networktocode.nautobot.console_server_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console Server Port Template
        device_type: Test Device Type
        state: absent

    - name: Delete console server port template by id
      networktocode.nautobot.console_server_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
console_server_port_template:
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
    NB_CONSOLE_SERVER_PORT_TEMPLATES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            device_type=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            module_type=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    console_server_port_template = NautobotDcimModule(module, NB_CONSOLE_SERVER_PORT_TEMPLATES)
    console_server_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
