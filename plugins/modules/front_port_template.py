#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: front_port_template
short_description: Create, update or delete front port templates within Nautobot
description:
  - Creates, updates or removes front port templates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  api_version:
    description:
      - API Version Nautobot REST Api
    required: false
    type: str
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
  device_type:
    description:
      - The device type the front port template is attached to
    required: true
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the front port template
    required: true
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the front port template
    choices:
      - 8p8c
      - 8p6c
      - 8p4c
      - 8p2c
      - gg45
      - tera-4p
      - tera-2p
      - tera-1p
      - 110-punch
      - bnc
      - mrj21
      - st
      - sc
      - sc-apc
      - fc
      - lc
      - lc-apc
      - mtrj
      - mpo
      - lsh
      - lsh-apc
      - splice
      - cs
      - sn
    required: true
    type: str
    version_added: "3.0.0"
  rear_port_template:
    description:
      - The rear_port_template the front port template is attached to
    required: true
    type: raw
    version_added: "3.0.0"
  rear_port_template_position:
    description:
      - The position of the rear port template this front port template is connected to
    required: false
    type: int
    version_added: "3.0.0"
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
    version_added: "3.0.0"
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
    - name: Create front port template within Nautobot with only required information
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port Template
        device_type: Test Device Type
        type: bnc
        rear_port_template: Test Rear Port Template
        state: present

    - name: Update front port template with other fields
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
        name: Test Front Port Template
        device_type: Test Device Type
        type: bnc
        rear_port_template: Test Rear Port Template
        rear_port_template_position: 5
        state: present

    - name: Delete front port template within nautobot
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port Template
        device_type: Test Device Type
        type: bnc
        rear_port_template: Test Rear Port Template
        state: absent
"""

RETURN = r"""
front_port_template:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_FRONT_PORT_TEMPLATES,
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
            device_type=dict(required=True, type="raw"),
            name=dict(required=True, type="str"),
            type=dict(
                required=True,
                choices=[
                    "8p8c",
                    "8p6c",
                    "8p4c",
                    "8p2c",
                    "gg45",
                    "tera-4p",
                    "tera-2p",
                    "tera-1p",
                    "110-punch",
                    "bnc",
                    "mrj21",
                    "st",
                    "sc",
                    "sc-apc",
                    "fc",
                    "lc",
                    "lc-apc",
                    "mtrj",
                    "mpo",
                    "lsh",
                    "lsh-apc",
                    "splice",
                    "cs",
                    "sn",
                ],
                type="str",
            ),
            rear_port_template=dict(required=True, type="raw"),
            rear_port_template_position=dict(required=False, type="int"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    front_port_template = NautobotDcimModule(module, NB_FRONT_PORT_TEMPLATES)
    front_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
