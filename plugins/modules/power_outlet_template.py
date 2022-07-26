#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_outlet_template
short_description: Create, update or delete power outlet templates within Nautobot
description:
  - Creates, updates or removes power outlet templates from Nautobot
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
      - API Version Nautobot REST API
    required: false
    type: str
    version_added: "4.1.0"
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
      - The device type the power outlet is attached to
    required: true
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the power outlet
    required: true
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the power outlet
    choices:
      - iec-60320-c5
      - iec-60320-c7
      - iec-60320-c13
      - iec-60320-c15
      - iec-60320-c19
      - iec-60309-p-n-e-4h
      - iec-60309-p-n-e-6h
      - iec-60309-p-n-e-9h
      - iec-60309-2p-e-4h
      - iec-60309-2p-e-6h
      - iec-60309-2p-e-9h
      - iec-60309-3p-e-4h
      - iec-60309-3p-e-6h
      - iec-60309-3p-e-9h
      - iec-60309-3p-n-e-4h
      - iec-60309-3p-n-e-6h
      - iec-60309-3p-n-e-9h
      - nema-5-15r
      - nema-5-20r
      - nema-5-30r
      - nema-5-50r
      - nema-6-15r
      - nema-6-20r
      - nema-6-30r
      - nema-6-50r
      - nema-l5-15r
      - nema-l5-20r
      - nema-l5-30r
      - nema-l5-50r
      - nema-l6-20r
      - nema-l6-30r
      - nema-l6-50r
      - nema-l14-20r
      - nema-l14-30r
      - nema-l21-20r
      - nema-l21-30r
      - CS6360C
      - CS6364C
      - CS8164C
      - CS8264C
      - CS8364C
      - CS8464C
      - ita-e
      - ita-f
      - ita-g
      - ita-h
      - ita-i
      - ita-j
      - ita-k
      - ita-l
      - ita-m
      - ita-n
      - ita-o
      - hdot-cx
    required: false
    type: str
    version_added: "3.0.0"
  power_port_template:
    description:
      - The attached power port
    required: false
    type: raw
    version_added: "3.0.0"
  feed_leg:
    description:
      - The phase, in case of three-phase feed
    choices:
      - A
      - B
      - C
    required: false
    type: str
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
    - name: Create power port within Nautobot with only required information
      networktocode.nautobot.power_outlet_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device_type: Test Device Type
        state: present

    - name: Update power port with other fields
      networktocode.nautobot.power_outlet_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device_type: Test Device Type
        type: iec-60320-c6
        power_port: Test Power Port
        feed_leg: A
        state: present

    - name: Delete power port within nautobot
      networktocode.nautobot.power_outlet_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device_type: Test Device Type
        state: absent
"""

RETURN = r"""
power_outlet_template:
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
    NB_POWER_OUTLET_TEMPLATES,
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
                required=False,
                choices=[
                    "iec-60320-c5",
                    "iec-60320-c7",
                    "iec-60320-c13",
                    "iec-60320-c15",
                    "iec-60320-c19",
                    "iec-60309-p-n-e-4h",
                    "iec-60309-p-n-e-6h",
                    "iec-60309-p-n-e-9h",
                    "iec-60309-2p-e-4h",
                    "iec-60309-2p-e-6h",
                    "iec-60309-2p-e-9h",
                    "iec-60309-3p-e-4h",
                    "iec-60309-3p-e-6h",
                    "iec-60309-3p-e-9h",
                    "iec-60309-3p-n-e-4h",
                    "iec-60309-3p-n-e-6h",
                    "iec-60309-3p-n-e-9h",
                    "nema-5-15r",
                    "nema-5-20r",
                    "nema-5-30r",
                    "nema-5-50r",
                    "nema-6-15r",
                    "nema-6-20r",
                    "nema-6-30r",
                    "nema-6-50r",
                    "nema-l5-15r",
                    "nema-l5-20r",
                    "nema-l5-30r",
                    "nema-l5-50r",
                    "nema-l6-20r",
                    "nema-l6-30r",
                    "nema-l6-50r",
                    "nema-l14-20r",
                    "nema-l14-30r",
                    "nema-l21-20r",
                    "nema-l21-30r",
                    "CS6360C",
                    "CS6364C",
                    "CS8164C",
                    "CS8264C",
                    "CS8364C",
                    "CS8464C",
                    "ita-e",
                    "ita-f",
                    "ita-g",
                    "ita-h",
                    "ita-i",
                    "ita-j",
                    "ita-k",
                    "ita-l",
                    "ita-m",
                    "ita-n",
                    "ita-o",
                    "hdot-cx",
                ],
                type="str",
            ),
            power_port_template=dict(required=False, type="raw"),
            feed_leg=dict(required=False, choices=["A", "B", "C"], type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_outlet_template = NautobotDcimModule(module, NB_POWER_OUTLET_TEMPLATES)
    power_outlet_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
