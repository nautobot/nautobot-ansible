#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cable
short_description: Creates or removes cables from Nautobot
description:
  - Creates or removes cables from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  termination_a_type:
    required: true
    type: str
  termination_b_type:
    required: true
    type: str
  termination_a_id:
    required: true
    type: str
  termination_b_id:
    required: true
    type: str
  type:
    required: false
    type: str
    choices:
      - "cat3"
      - "cat5"
      - "cat5e"
      - "cat6"
      - "cat6a"
      - "cat7"
      - "cat7a"
      - "cat8"
      - "dac-active"
      - "dac-passive"
      - "mrj21-trunk"
      - "coaxial"
      - "mmf"
      - "mmf-om1"
      - "mmf-om2"
      - "mmf-om3"
      - "mmf-om4"
      - "mmf-om5"
      - "smf"
      - "smf-os1"
      - "smf-os2"
      - "aoc"
      - "power"
      - "other"
  label:
    required: false
    type: str
  color:
    required: false
    type: str
  length:
    required: false
    type: int
  length_unit:
    required: false
    type: str
    choices:
      - "km"
      - "m"
      - "cm"
      - "mi"
      - "ft"
      - "in"
  status:
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create cable within Nautobot with only required information
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
        termination_a_type: "Test termination_a_type"
        termination_b_type: "Test termination_b_type"
        termination_a_id: "Test termination_a_id"
        termination_b_id: "Test termination_b_id"
        status: "Active"
        state: present

    - name: Delete cable within nautobot
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
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

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_CABLES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            termination_a_type=dict(required=True, type="str"),
            termination_b_type=dict(required=True, type="str"),
            termination_a_id=dict(required=True, type="str"),
            termination_b_id=dict(required=True, type="str"),
            type=dict(
                required=False,
                type="str",
                choices=[
                    "cat3",
                    "cat5",
                    "cat5e",
                    "cat6",
                    "cat6a",
                    "cat7",
                    "cat7a",
                    "cat8",
                    "dac-active",
                    "dac-passive",
                    "mrj21-trunk",
                    "coaxial",
                    "mmf",
                    "mmf-om1",
                    "mmf-om2",
                    "mmf-om3",
                    "mmf-om4",
                    "mmf-om5",
                    "smf",
                    "smf-os1",
                    "smf-os2",
                    "aoc",
                    "power",
                    "other",
                ],
            ),
            label=dict(required=False, type="str"),
            color=dict(required=False, type="str"),
            length=dict(required=False, type="int"),
            length_unit=dict(
                required=False,
                type="str",
                choices=[
                    "km",
                    "m",
                    "cm",
                    "mi",
                    "ft",
                    "in",
                ],
            ),
            status=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    cable = NautobotDcimModule(module, NB_CABLES)
    cable.run()


if __name__ == "__main__":  # pragma: no cover
    main()
