#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: console_port_template
short_description: Creates or removes console port templates from Nautobot
description:
  - Creates or removes console port templates from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  label:
    required: false
    type: str
  description:
    required: false
    type: str
  type:
    required: false
    type: str
    choices:
      - "de-9"
      - "db-25"
      - "rj-11"
      - "rj-12"
      - "rj-45"
      - "mini-din-8"
      - "usb-a"
      - "usb-b"
      - "usb-c"
      - "usb-mini-a"
      - "usb-mini-b"
      - "usb-micro-a"
      - "usb-micro-b"
      - "usb-micro-ab"
      - "other"
  device_type:
    required: false
    type: dict
  module_type:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create console port template within Nautobot with only required information
      networktocode.nautobot.console_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console Port Template
        state: present

    - name: Delete console_port_template within nautobot
      networktocode.nautobot.console_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console_Port_Template
        state: absent
"""

RETURN = r"""
console_port_template:
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
    NB_CONSOLE_PORT_TEMPLATES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            type=dict(
                required=False,
                type="str",
                choices=[
                    "de-9",
                    "db-25",
                    "rj-11",
                    "rj-12",
                    "rj-45",
                    "mini-din-8",
                    "usb-a",
                    "usb-b",
                    "usb-c",
                    "usb-mini-a",
                    "usb-mini-b",
                    "usb-micro-a",
                    "usb-micro-b",
                    "usb-micro-ab",
                    "other",
                ],
            ),
            device_type=dict(required=False, type="dict"),
            module_type=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    console_port_template = NautobotDcimModule(module, NB_CONSOLE_PORT_TEMPLATES)
    console_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
