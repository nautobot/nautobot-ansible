#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: circuit
short_description: Creates or removes circuits from Nautobot
description:
  - Creates or removes circuits from Nautobot
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
  cid:
    required: true
    type: str
  install_date:
    required: false
    type: str
  commit_rate:
    required: false
    type: int
  description:
    required: false
    type: str
  comments:
    required: false
    type: str
  status:
    required: true
    type: str
  provider:
    required: true
    type: dict
  circuit_type:
    required: true
    type: dict
  tenant:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create circuit within Nautobot with only required information
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        cid: "Test cid"
        status: "Active"
        provider: None
        circuit_type: None
        state: present

    - name: Delete circuit within nautobot
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
circuit:
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
    NautobotCircuitsModule,
    NB_CIRCUITS,
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
            cid=dict(required=True, type="str"),
            install_date=dict(required=False, type="str"),
            commit_rate=dict(required=False, type="int"),
            description=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
            status=dict(required=True, type="str"),
            provider=dict(required=True, type="dict"),
            circuit_type=dict(required=True, type="dict"),
            tenant=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    circuit = NautobotCircuitsModule(module, NB_CIRCUITS)
    circuit.run()


if __name__ == "__main__":  # pragma: no cover
    main()
