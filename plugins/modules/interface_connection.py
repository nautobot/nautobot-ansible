#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: interface_connection
short_description: Creates or removes interface connections from Nautobot
description:
  - Creates or removes interface connections from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create interface_connection within Nautobot with only required information
      networktocode.nautobot.interface_connection:
        url: http://nautobot.local
        token: thisIsMyToken
        state: present

    - name: Delete interface_connection within nautobot
      networktocode.nautobot.interface_connection:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
interface_connection:
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
    NB_INTERFACE_CONNECTIONS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    interface_connection = NautobotDcimModule(module, NB_INTERFACE_CONNECTIONS)
    interface_connection.run()


if __name__ == "__main__":  # pragma: no cover
    main()
