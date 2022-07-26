#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cable
short_description: Create, update or delete cables within Nautobot
description:
  - Creates, updates or removes cables from Nautobot
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
  termination_a_type:
    description:
      - The type of the termination a
    choices:
      - circuits.circuittermination
      - dcim.consoleport
      - dcim.consoleserverport
      - dcim.frontport
      - dcim.interface
      - dcim.powerfeed
      - dcim.poweroutlet
      - dcim.powerport
      - dcim.rearport
    required: true
    type: str
    version_added: "3.0.0"
  termination_a:
    description:
      - The termination a
    required: true
    type: raw
    version_added: "3.0.0"
  termination_b_type:
    description:
      - The type of the termination b
    choices:
      - circuits.circuittermination
      - dcim.consoleport
      - dcim.consoleserverport
      - dcim.frontport
      - dcim.interface
      - dcim.powerfeed
      - dcim.poweroutlet
      - dcim.powerport
      - dcim.rearport
    required: true
    type: str
    version_added: "3.0.0"
  termination_b:
    description:
      - The termination b
    required: true
    type: raw
    version_added: "3.0.0"
  type:
    description:
      - The type of the cable
    choices:
      - cat3
      - cat5
      - cat5e
      - cat6
      - cat6a
      - cat7
      - dac-active
      - dac-passive
      - mrj21-trunk
      - coaxial
      - mmf
      - mmf-om1
      - mmf-om2
      - mmf-om3
      - mmf-om4
      - smf
      - smf-os1
      - smf-os2
      - aoc
      - power
    required: false
    type: str
    version_added: "3.0.0"
  status:
    description:
      - The status of the cable
      - Required if I(state=present) and does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  label:
    description:
      - The label of the cable
    required: false
    type: str
    version_added: "3.0.0"
  color:
    description:
      - The color of the cable
    required: false
    type: str
    version_added: "3.0.0"
  length:
    description:
      - The length of the cable
    required: false
    type: int
    version_added: "3.0.0"
  length_unit:
    version_added: "3.0.0"
    description:
      - The unit in which the length of the cable is measured
    choices:
      - m
      - cm
      - ft
      - in
    required: false
    type: str
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    version_added: "3.0.0"
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
    - name: Create cable within Nautobot with only required information
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
        termination_a_type: dcim.interface
        termination_a:
          device: Test Nexus Child One
          name: Ethernet2/2
        termination_b_type: dcim.interface
        termination_b:
          device: Test Nexus Child One
          name: Ethernet2/1
        status: active
        state: present

    - name: Update cable with other fields
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
        termination_a_type: dcim.interface
        termination_a:
          device: Test Nexus Child One
          name: Ethernet2/2
        termination_b_type: dcim.interface
        termination_b:
          device: Test Nexus Child One
          name: Ethernet2/1
        type: mmf-om4
        status: planned
        label: label123
        color: abcdef
        length: 30
        length_unit: m
        state: present

    - name: Delete cable within nautobot
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
        termination_a_type: dcim.interface
        termination_a:
          device: Test Nexus Child One
          name: Ethernet2/2
        termination_b_type: dcim.interface
        termination_b:
          device: Test Nexus Child One
          name: Ethernet2/1
        state: absent
"""

RETURN = r"""
cable:
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
    NB_CABLES,
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
            termination_a_type=dict(
                required=True,
                choices=[
                    "circuits.circuittermination",
                    "dcim.consoleport",
                    "dcim.consoleserverport",
                    "dcim.frontport",
                    "dcim.interface",
                    "dcim.powerfeed",
                    "dcim.poweroutlet",
                    "dcim.powerport",
                    "dcim.rearport",
                ],
                type="str",
            ),
            termination_a=dict(required=True, type="raw"),
            termination_b_type=dict(
                required=True,
                choices=[
                    "circuits.circuittermination",
                    "dcim.consoleport",
                    "dcim.consoleserverport",
                    "dcim.frontport",
                    "dcim.interface",
                    "dcim.powerfeed",
                    "dcim.poweroutlet",
                    "dcim.powerport",
                    "dcim.rearport",
                ],
                type="str",
            ),
            termination_b=dict(required=True, type="raw"),
            type=dict(
                required=False,
                choices=[
                    "cat3",
                    "cat5",
                    "cat5e",
                    "cat6",
                    "cat6a",
                    "cat7",
                    "dac-active",
                    "dac-passive",
                    "mrj21-trunk",
                    "coaxial",
                    "mmf",
                    "mmf-om1",
                    "mmf-om2",
                    "mmf-om3",
                    "mmf-om4",
                    "smf",
                    "smf-os1",
                    "smf-os2",
                    "aoc",
                    "power",
                ],
                type="str",
            ),
            status=dict(
                required=False,
                type="str",
            ),
            label=dict(required=False, type="str"),
            color=dict(required=False, type="str"),
            length=dict(required=False, type="int"),
            length_unit=dict(required=False, choices=["m", "cm", "ft", "in"], type="str"),
        )
    )

    required_if = [
        (
            "state",
            "present",
            ["termination_a_type", "termination_a", "termination_b_type", "termination_b", "status"],
        ),
        ("state", "absent", ["termination_a_type", "termination_a", "termination_b_type", "termination_b"]),
    ]

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    cable = NautobotDcimModule(module, NB_CABLES)
    cable.run()


if __name__ == "__main__":  # pragma: no cover
    main()
