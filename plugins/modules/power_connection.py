#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_connection
short_description: Creates or removes power connections from Nautobot
description:
  - Creates or removes power connections from Nautobot
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
    - name: Create power connection within Nautobot with only required information
      networktocode.nautobot.power_connection:
        url: http://nautobot.local
        token: thisIsMyToken
        state: present

    - name: Delete power_connection within nautobot
      networktocode.nautobot.power_connection:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
power_connection:
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
    NB_POWER_CONNECTIONS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_connection = NautobotDcimModule(module, NB_POWER_CONNECTIONS)
    power_connection.run()


if __name__ == "__main__":  # pragma: no cover
    main()
