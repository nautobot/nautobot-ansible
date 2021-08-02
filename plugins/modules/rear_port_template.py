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
module: rear_port_template
short_description: Create, update or delete rear port templates within Nautobot
description:
  - Creates, updates or removes rear port templates from Nautobot
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
  data:
    type: dict
    required: true
    description:
      - Defines the rear port template configuration
    suboptions:
      device_type:
        description:
          - The device type the rear port template is attached to
        required: true
        type: raw
      name:
        description:
          - The name of the rear port template
        required: true
        type: str
      type:
        description:
          - The type of the rear port
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
        required: false
        type: str
      positions:
        description:
          - The number of front ports which may be mapped to each rear port
        required: false
        type: int
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
    - name: Create rear port template within Nautobot with only required information
      networktocode.nautobot.rear_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Rear Port Template
          device_type: Test Device Type
          type: bnc
        state: present

    - name: Update rear port template with other fields
      networktocode.nautobot.rear_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Rear Port Template
          device_type: Test Device Type
          type: bnc
          positions: 5
        state: present

    - name: Delete rear port template within nautobot
      networktocode.nautobot.rear_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotAnsibleModule,
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_REAR_PORT_TEMPLATES,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    device_type=dict(required=True, type="raw"),
                    name=dict(required=True, type="str"),
                    type=dict(
                        required=False,
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
                    positions=dict(required=False, type="int"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["device_type", "name", "type"]),
        ("state", "absent", ["device_type", "name", "type"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    rear_port_template = NautobotDcimModule(module, NB_REAR_PORT_TEMPLATES)
    rear_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
