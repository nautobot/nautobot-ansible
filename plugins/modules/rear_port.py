#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rear_port
short_description: Creates or removes rear ports from Nautobot
description:
  - Creates or removes rear ports from Nautobot
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
    required: true
    type: str
    choices:
      - "8p8c"
      - "8p6c"
      - "8p4c"
      - "8p2c"
      - "6p6c"
      - "6p4c"
      - "6p2c"
      - "4p4c"
      - "4p2c"
      - "gg45"
      - "tera-4p"
      - "tera-2p"
      - "tera-1p"
      - "110-punch"
      - "bnc"
      - "f"
      - "n"
      - "mrj21"
      - "fc"
      - "lc"
      - "lc-pc"
      - "lc-upc"
      - "lc-apc"
      - "lsh"
      - "lsh-pc"
      - "lsh-upc"
      - "lsh-apc"
      - "lx5"
      - "lx5-pc"
      - "lx5-upc"
      - "lx5-apc"
      - "mpo"
      - "mtrj"
      - "sc"
      - "sc-pc"
      - "sc-upc"
      - "sc-apc"
      - "st"
      - "cs"
      - "sn"
      - "sma-905"
      - "sma-906"
      - "urm-p2"
      - "urm-p4"
      - "urm-p8"
      - "splice"
      - "other"
  positions:
    required: false
    type: int
  device:
    required: false
    type: dict
  module:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create rear_port within Nautobot with only required information
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear_Port
        type: 8p8c
        state: present

    - name: Delete rear_port within nautobot
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear_Port
        state: absent
"""

RETURN = r"""
rear_port:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_REAR_PORTS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            type=dict(
                required=True,
                type="str",
                choices=[
                    "8p8c",
                    "8p6c",
                    "8p4c",
                    "8p2c",
                    "6p6c",
                    "6p4c",
                    "6p2c",
                    "4p4c",
                    "4p2c",
                    "gg45",
                    "tera-4p",
                    "tera-2p",
                    "tera-1p",
                    "110-punch",
                    "bnc",
                    "f",
                    "n",
                    "mrj21",
                    "fc",
                    "lc",
                    "lc-pc",
                    "lc-upc",
                    "lc-apc",
                    "lsh",
                    "lsh-pc",
                    "lsh-upc",
                    "lsh-apc",
                    "lx5",
                    "lx5-pc",
                    "lx5-upc",
                    "lx5-apc",
                    "mpo",
                    "mtrj",
                    "sc",
                    "sc-pc",
                    "sc-upc",
                    "sc-apc",
                    "st",
                    "cs",
                    "sn",
                    "sma-905",
                    "sma-906",
                    "urm-p2",
                    "urm-p4",
                    "urm-p8",
                    "splice",
                    "other",
                ],
            ),
            positions=dict(required=False, type="int"),
            device=dict(required=False, type="dict"),
            module=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rear_port = NautobotDcimModule(module, NB_REAR_PORTS)
    rear_port.run()


if __name__ == "__main__":  # pragma: no cover
    main()
