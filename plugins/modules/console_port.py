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
module: console_port
short_description: Create, update or delete console ports within Nautobot
description:
  - Creates, updates or removes console ports from Nautobot
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
  device:
    description:
      - The device the console port is attached to
    required: true
    type: raw
  name:
    description:
      - The name of the console port
    required: true
    type: str
  type:
    description:
      - The type of the console port
    choices:
      - de-9
      - db-25
      - rj-11
      - rj-12
      - rj-45
      - usb-a
      - usb-b
      - usb-c
      - usb-mini-a
      - usb-mini-b
      - usb-micro-a
      - usb-micro-b
      - other
    required: false
    type: str
  description:
    description:
      - Description of the console port
    required: false
    type: str
  tags:
    description:
      - Any tags that the console port may need to be associated with
    required: false
    type: list
    elements: raw
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
    - name: Create console port within Nautobot with only required information
      networktocode.nautobot.console_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console Port
        device: Test Device
        state: present

    - name: Update console port with other fields
      networktocode.nautobot.console_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console Port
        device: Test Device
        type: usb-a
        description: console port description
        state: present

    - name: Delete console port within nautobot
      networktocode.nautobot.console_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Console Port
        device: Test Device
        state: absent
"""

RETURN = r"""
console_port:
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
    NB_CONSOLE_PORTS,
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
            device=dict(required=True, type="raw"),
            name=dict(required=True, type="str"),
            type=dict(
                required=False,
                choices=[
                    "de-9",
                    "db-25",
                    "rj-11",
                    "rj-12",
                    "rj-45",
                    "usb-a",
                    "usb-b",
                    "usb-c",
                    "usb-mini-a",
                    "usb-mini-b",
                    "usb-micro-a",
                    "usb-micro-b",
                    "other",
                ],
                type="str",
            ),
            description=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    console_port = NautobotDcimModule(module, NB_CONSOLE_PORTS)
    console_port.run()


if __name__ == "__main__":  # pragma: no cover
    main()
