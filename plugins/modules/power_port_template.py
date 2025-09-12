#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_port_template
short_description: Creates or removes power port templates from Nautobot
description:
  - Creates or removes power port templates from Nautobot
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
      - "iec-60320-c6"
      - "iec-60320-c8"
      - "iec-60320-c14"
      - "iec-60320-c16"
      - "iec-60320-c20"
      - "iec-60320-c22"
      - "iec-60309-p-n-e-4h"
      - "iec-60309-p-n-e-6h"
      - "iec-60309-p-n-e-9h"
      - "iec-60309-2p-e-4h"
      - "iec-60309-2p-e-6h"
      - "iec-60309-2p-e-9h"
      - "iec-60309-3p-e-4h"
      - "iec-60309-3p-e-6h"
      - "iec-60309-3p-e-9h"
      - "iec-60309-3p-n-e-4h"
      - "iec-60309-3p-n-e-6h"
      - "iec-60309-3p-n-e-9h"
      - "iec-60906-1"
      - "nbr-14136-10a"
      - "nbr-14136-20a"
      - "nema-1-15p"
      - "nema-5-15p"
      - "nema-5-20p"
      - "nema-5-30p"
      - "nema-5-50p"
      - "nema-6-15p"
      - "nema-6-20p"
      - "nema-6-30p"
      - "nema-6-50p"
      - "nema-10-30p"
      - "nema-10-50p"
      - "nema-14-20p"
      - "nema-14-30p"
      - "nema-14-50p"
      - "nema-14-60p"
      - "nema-15-15p"
      - "nema-15-20p"
      - "nema-15-30p"
      - "nema-15-50p"
      - "nema-15-60p"
      - "nema-l1-15p"
      - "nema-l5-15p"
      - "nema-l5-20p"
      - "nema-l5-30p"
      - "nema-l5-50p"
      - "nema-l6-15p"
      - "nema-l6-20p"
      - "nema-l6-30p"
      - "nema-l6-50p"
      - "nema-l10-30p"
      - "nema-l14-20p"
      - "nema-l14-30p"
      - "nema-l14-50p"
      - "nema-l14-60p"
      - "nema-l15-20p"
      - "nema-l15-30p"
      - "nema-l15-50p"
      - "nema-l15-60p"
      - "nema-l21-20p"
      - "nema-l21-30p"
      - "nema-l22-30p"
      - "cs6361c"
      - "cs6365c"
      - "cs8165c"
      - "cs8265c"
      - "cs8365c"
      - "cs8465c"
      - "ita-c"
      - "ita-e"
      - "ita-f"
      - "ita-ef"
      - "ita-g"
      - "ita-h"
      - "ita-i"
      - "ita-j"
      - "ita-k"
      - "ita-l"
      - "ita-m"
      - "ita-n"
      - "ita-o"
      - "usb-a"
      - "usb-b"
      - "usb-c"
      - "usb-mini-a"
      - "usb-mini-b"
      - "usb-micro-a"
      - "usb-micro-b"
      - "usb-micro-ab"
      - "usb-3-b"
      - "usb-3-micro-b"
      - "dc-terminal"
      - "saf-d-grid"
      - "neutrik-powercon-20"
      - "neutrik-powercon-32"
      - "neutrik-powercon-true1"
      - "neutrik-powercon-true1-top"
      - "ubiquiti-smartpower"
      - "hardwired"
      - "other"
  maximum_draw:
    required: false
    type: int
  allocated_draw:
    required: false
    type: int
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
    - name: Create power_port_template within Nautobot with only required information
      networktocode.nautobot.power_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power_Port_Template
        state: present

    - name: Delete power_port_template within nautobot
      networktocode.nautobot.power_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power_Port_Template
        state: absent
"""

RETURN = r"""
power_port_template:
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
    NB_POWER_PORT_TEMPLATES,
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
                    "iec-60320-c6",
                    "iec-60320-c8",
                    "iec-60320-c14",
                    "iec-60320-c16",
                    "iec-60320-c20",
                    "iec-60320-c22",
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
                    "iec-60906-1",
                    "nbr-14136-10a",
                    "nbr-14136-20a",
                    "nema-1-15p",
                    "nema-5-15p",
                    "nema-5-20p",
                    "nema-5-30p",
                    "nema-5-50p",
                    "nema-6-15p",
                    "nema-6-20p",
                    "nema-6-30p",
                    "nema-6-50p",
                    "nema-10-30p",
                    "nema-10-50p",
                    "nema-14-20p",
                    "nema-14-30p",
                    "nema-14-50p",
                    "nema-14-60p",
                    "nema-15-15p",
                    "nema-15-20p",
                    "nema-15-30p",
                    "nema-15-50p",
                    "nema-15-60p",
                    "nema-l1-15p",
                    "nema-l5-15p",
                    "nema-l5-20p",
                    "nema-l5-30p",
                    "nema-l5-50p",
                    "nema-l6-15p",
                    "nema-l6-20p",
                    "nema-l6-30p",
                    "nema-l6-50p",
                    "nema-l10-30p",
                    "nema-l14-20p",
                    "nema-l14-30p",
                    "nema-l14-50p",
                    "nema-l14-60p",
                    "nema-l15-20p",
                    "nema-l15-30p",
                    "nema-l15-50p",
                    "nema-l15-60p",
                    "nema-l21-20p",
                    "nema-l21-30p",
                    "nema-l22-30p",
                    "cs6361c",
                    "cs6365c",
                    "cs8165c",
                    "cs8265c",
                    "cs8365c",
                    "cs8465c",
                    "ita-c",
                    "ita-e",
                    "ita-f",
                    "ita-ef",
                    "ita-g",
                    "ita-h",
                    "ita-i",
                    "ita-j",
                    "ita-k",
                    "ita-l",
                    "ita-m",
                    "ita-n",
                    "ita-o",
                    "usb-a",
                    "usb-b",
                    "usb-c",
                    "usb-mini-a",
                    "usb-mini-b",
                    "usb-micro-a",
                    "usb-micro-b",
                    "usb-micro-ab",
                    "usb-3-b",
                    "usb-3-micro-b",
                    "dc-terminal",
                    "saf-d-grid",
                    "neutrik-powercon-20",
                    "neutrik-powercon-32",
                    "neutrik-powercon-true1",
                    "neutrik-powercon-true1-top",
                    "ubiquiti-smartpower",
                    "hardwired",
                    "other",
                ],
            ),
            maximum_draw=dict(required=False, type="int"),
            allocated_draw=dict(required=False, type="int"),
            device_type=dict(required=False, type="dict"),
            module_type=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_port_template = NautobotDcimModule(module, NB_POWER_PORT_TEMPLATES)
    power_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
