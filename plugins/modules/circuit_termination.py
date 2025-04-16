#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: circuit_termination
short_description: Create, update or delete circuit terminations within Nautobot
description:
  - Creates, updates or removes circuit terminations from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  circuit:
    description:
      - The circuit to assign to circuit termination
    required: true
    version_added: "3.0.0"
    type: raw
  term_side:
    version_added: "3.0.0"
    description:
      - The side of the circuit termination
    choices:
      - A
      - Z
    required: true
    type: str
  location:
    version_added: "3.0.0"
    description:
      - The location the circuit termination will be assigned to
    required: false
    type: raw
  port_speed:
    version_added: "3.0.0"
    description:
      - The speed of the port (Kbps)
    required: false
    type: int
  upstream_speed:
    version_added: "3.0.0"
    description:
      - The upstream speed of the circuit termination
    required: false
    type: int
  xconnect_id:
    version_added: "3.0.0"
    description:
      - The cross connect ID of the circuit termination
    required: false
    type: str
  pp_info:
    version_added: "3.0.0"
    description:
      - Patch panel information
    required: false
    type: str
  description:
    version_added: "3.0.0"
    description:
      - Description of the circuit termination
    required: false
    type: str
  provider_network:
    version_added: "4.2.0"
    description:
      - Connection to a provider_network type
    type: raw
    required: false
  cloud_network:
    version_added: "5.4.0"
    description:
      - Connection to a cloud_network type
    type: raw
    required: false
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create circuit termination within Nautobot with only required information
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: A
        location:
          name: My Location
          parent: Parent Location
        port_speed: 10000
        state: present

    - name: Create circuit termination to Provider Network
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: Z
        provider_network:
          name: "Provider A"
        port_speed: 10000
        state: present

    - name: Update circuit termination with other fields
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: A
        upstream_speed: 1000
        xconnect_id: 10X100
        pp_info: PP10-24
        description: "Test description"
        state: present

    - name: Delete circuit termination within nautobot
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: A
        state: absent
"""

RETURN = r"""
circuit_termination:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.circuits import (
    NB_CIRCUIT_TERMINATIONS,
    NautobotCircuitsModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            circuit=dict(required=True, type="raw"),
            term_side=dict(required=True, choices=["A", "Z"]),
            location=dict(required=False, type="raw"),
            port_speed=dict(required=False, type="int"),
            upstream_speed=dict(required=False, type="int"),
            xconnect_id=dict(required=False, type="str"),
            pp_info=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            provider_network=dict(required=False, type="raw"),
            cloud_network=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    circuit_termination = NautobotCircuitsModule(module, NB_CIRCUIT_TERMINATIONS)
    circuit_termination.run()


if __name__ == "__main__":  # pragma: no cover
    main()
