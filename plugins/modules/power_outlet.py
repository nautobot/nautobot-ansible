#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_outlet
short_description: Creates or removes power outlets from Nautobot
description:
  - Creates or removes power outlets from Nautobot
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
    required: false
    type: str
    choices:
      - "CS6360C"
      - "CS6364C"
      - "CS8164C"
      - "CS8264C"
      - "CS8364C"
      - "CS8464C"
      - "dc-terminal"
      - "eaton-c39"
      - "hardwired"
      - "hdot-cx"
      - "iec-60309-2p-e-4h"
      - "iec-60309-2p-e-6h"
      - "iec-60309-2p-e-9h"
      - "iec-60309-3p-e-4h"
      - "iec-60309-3p-e-6h"
      - "iec-60309-3p-e-9h"
      - "iec-60309-3p-n-e-4h"
      - "iec-60309-3p-n-e-6h"
      - "iec-60309-3p-n-e-9h"
      - "iec-60309-p-n-e-4h"
      - "iec-60309-p-n-e-6h"
      - "iec-60309-p-n-e-9h"
      - "iec-60320-c13"
      - "iec-60320-c15"
      - "iec-60320-c19"
      - "iec-60320-c21"
      - "iec-60320-c5"
      - "iec-60320-c7"
      - "iec-60906-1"
      - "ita-e"
      - "ita-f"
      - "ita-g"
      - "ita-h"
      - "ita-i"
      - "ita-j"
      - "ita-k"
      - "ita-l"
      - "ita-m"
      - "ita-multistandard"
      - "ita-n"
      - "ita-o"
      - "nbr-14136-10a"
      - "nbr-14136-20a"
      - "nema-1-15r"
      - "nema-10-30r"
      - "nema-10-50r"
      - "nema-14-20r"
      - "nema-14-30r"
      - "nema-14-50r"
      - "nema-14-60r"
      - "nema-15-15r"
      - "nema-15-20r"
      - "nema-15-30r"
      - "nema-15-50r"
      - "nema-15-60r"
      - "nema-5-15r"
      - "nema-5-20r"
      - "nema-5-30r"
      - "nema-5-50r"
      - "nema-6-15r"
      - "nema-6-20r"
      - "nema-6-30r"
      - "nema-6-50r"
      - "nema-l1-15r"
      - "nema-l10-30r"
      - "nema-l14-20r"
      - "nema-l14-30r"
      - "nema-l14-50r"
      - "nema-l14-60r"
      - "nema-l15-20r"
      - "nema-l15-30r"
      - "nema-l15-50r"
      - "nema-l15-60r"
      - "nema-l21-20r"
      - "nema-l21-30r"
      - "nema-l22-30r"
      - "nema-l5-15r"
      - "nema-l5-20r"
      - "nema-l5-30r"
      - "nema-l5-50r"
      - "nema-l6-15r"
      - "nema-l6-20r"
      - "nema-l6-30r"
      - "nema-l6-50r"
      - "neutrik-powercon-20a"
      - "neutrik-powercon-32a"
      - "neutrik-powercon-true1"
      - "neutrik-powercon-true1-top"
      - "other"
      - "saf-d-grid"
      - "ubiquiti-smartpower"
      - "usb-a"
      - "usb-c"
      - "usb-micro-b"
  feed_leg:
    required: false
    type: str
    choices:
      - "A"
      - "B"
      - "C"
  device:
    required: false
    type: dict
  module:
    required: false
    type: dict
  power_port:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create power outlet within Nautobot with only required information
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        state: present

    - name: Delete power_outlet within nautobot
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        state: absent
"""

RETURN = r"""
power_outlet:
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
    NB_POWER_OUTLETS,
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
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            type=dict(
                required=False,
                type="str",
                choices=[
                    "CS6360C",
                    "CS6364C",
                    "CS8164C",
                    "CS8264C",
                    "CS8364C",
                    "CS8464C",
                    "dc-terminal",
                    "eaton-c39",
                    "hardwired",
                    "hdot-cx",
                    "iec-60309-2p-e-4h",
                    "iec-60309-2p-e-6h",
                    "iec-60309-2p-e-9h",
                    "iec-60309-3p-e-4h",
                    "iec-60309-3p-e-6h",
                    "iec-60309-3p-e-9h",
                    "iec-60309-3p-n-e-4h",
                    "iec-60309-3p-n-e-6h",
                    "iec-60309-3p-n-e-9h",
                    "iec-60309-p-n-e-4h",
                    "iec-60309-p-n-e-6h",
                    "iec-60309-p-n-e-9h",
                    "iec-60320-c13",
                    "iec-60320-c15",
                    "iec-60320-c19",
                    "iec-60320-c21",
                    "iec-60320-c5",
                    "iec-60320-c7",
                    "iec-60906-1",
                    "ita-e",
                    "ita-f",
                    "ita-g",
                    "ita-h",
                    "ita-i",
                    "ita-j",
                    "ita-k",
                    "ita-l",
                    "ita-m",
                    "ita-multistandard",
                    "ita-n",
                    "ita-o",
                    "nbr-14136-10a",
                    "nbr-14136-20a",
                    "nema-1-15r",
                    "nema-10-30r",
                    "nema-10-50r",
                    "nema-14-20r",
                    "nema-14-30r",
                    "nema-14-50r",
                    "nema-14-60r",
                    "nema-15-15r",
                    "nema-15-20r",
                    "nema-15-30r",
                    "nema-15-50r",
                    "nema-15-60r",
                    "nema-5-15r",
                    "nema-5-20r",
                    "nema-5-30r",
                    "nema-5-50r",
                    "nema-6-15r",
                    "nema-6-20r",
                    "nema-6-30r",
                    "nema-6-50r",
                    "nema-l1-15r",
                    "nema-l10-30r",
                    "nema-l14-20r",
                    "nema-l14-30r",
                    "nema-l14-50r",
                    "nema-l14-60r",
                    "nema-l15-20r",
                    "nema-l15-30r",
                    "nema-l15-50r",
                    "nema-l15-60r",
                    "nema-l21-20r",
                    "nema-l21-30r",
                    "nema-l22-30r",
                    "nema-l5-15r",
                    "nema-l5-20r",
                    "nema-l5-30r",
                    "nema-l5-50r",
                    "nema-l6-15r",
                    "nema-l6-20r",
                    "nema-l6-30r",
                    "nema-l6-50r",
                    "neutrik-powercon-20a",
                    "neutrik-powercon-32a",
                    "neutrik-powercon-true1",
                    "neutrik-powercon-true1-top",
                    "other",
                    "saf-d-grid",
                    "ubiquiti-smartpower",
                    "usb-a",
                    "usb-c",
                    "usb-micro-b",
                ],
            ),
            feed_leg=dict(
                required=False,
                type="str",
                choices=[
                    "A",
                    "B",
                    "C",
                ],
            ),
            device=dict(required=False, type="dict"),
            module=dict(required=False, type="dict"),
            power_port=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_outlet = NautobotDcimModule(module, NB_POWER_OUTLETS)
    power_outlet.run()


if __name__ == "__main__":  # pragma: no cover
    main()
