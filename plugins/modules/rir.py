#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rir
short_description: Create, update or delete RIRs within Nautobot
description:
  - Creates, updates or removes RIRs from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  name:
    description:
      - The name of the RIR
    required: true
    type: str
    version_added: "3.0.0"
  is_private:
    description:
      - IP space managed by this RIR is considered private
    required: false
    type: bool
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create RIR within Nautobot with only required information
      networktocode.nautobot.rir:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test RIR One
        state: present

    - name: Update Test RIR One
      networktocode.nautobot.rir:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test RIR One
        is_private: True
        state: present

    - name: Delete RIR within nautobot
      networktocode.nautobot.rir:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test RIR One
        state: absent
"""

RETURN = r"""
rir:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_RIRS,
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
            name=dict(required=True, type="str"),
            is_private=dict(required=False, type="bool"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rir = NautobotIpamModule(module, NB_RIRS)
    rir.run()


if __name__ == "__main__":  # pragma: no cover
    main()
