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
module: device_bay_template
short_description: Create, update or delete device bay templates within Nautobot
description:
  - Creates, updates or removes device bay templates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
requirements:
  - pynautobot
version_added: '0.3.0'
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
      - Defines the device bay template configuration
    suboptions:
      device_type:
        description:
          - The device type the device bay template will be associated to. The device type must be "parent".
        required: true
        type: raw
      name:
        description:
          - The name of the device bay template
        required: true
        type: str
    type: dict
    required: true
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
    - name: Create device bay template within Nautobot with only required information
      device_bay_template:
        url: http://netbox.local
        token: thisIsMyToken
        data:
          name: device bay template One
          device_type: Device Type One
        state: present

    - name: Delete device bay template within netbox
      device_bay_template:
        url: http://netbox.local
        token: thisIsMyToken
        data:
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_DEVICE_BAY_TEMPLATES,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    device_type=dict(required=True, type="raw"),
                    name=dict(required=True, type="str"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["name", "device_type"]),
        ("state", "absent", ["name", "device_type"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    device_bay_template = NautobotDcimModule(module, NB_DEVICE_BAY_TEMPLATES)
    device_bay_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
