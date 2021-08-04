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
module: device_interface_template
short_description: Creates or removes interfaces on devices from Nautobot
description:
  - Creates or removes interfaces from Nautobot
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
    description:
      - Defines the prefix configuration
    suboptions:
      device_type:
        description:
          - Name of the device the interface template will be associated with (case-sensitive)
        required: true
        type: raw
      name:
        description:
          - Name of the interface template to be created
        required: true
        type: str
      type:
        description:
          - |
            Form factor of the interface:
            ex. 1000Base-T (1GE), Virtual, 10GBASE-T (10GE)
            This has to be specified exactly as what is found within UI
        required: true
        type: str
      mgmt_only:
        description:
          - This interface template is used only for out-of-band management
        required: false
        type: bool
    required: true
    type: dict
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
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot interface template module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create interface template within Nautobot with only required information
      networktocode.nautobot.device_interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          device_type: Arista Test
          name: 10GBASE-T (10GE)
          type: 10gbase-t
        state: present
    - name: Delete interface template within nautobot
      networktocode.nautobot.device_interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          device_type: Arista Test
          name: 10GBASE-T (10GE)
          type: 10gbase-t
        state: absent
"""

RETURN = r"""
interface_template:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
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
    NB_INTERFACE_TEMPLATES,
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
                    type=dict(required=True, type="str",),
                    mgmt_only=dict(required=False, type="bool"),
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

    device_interface_template = NautobotDcimModule(module, NB_INTERFACE_TEMPLATES)
    device_interface_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
