#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: connected_device
short_description: Creates or removes connected device from Nautobot
description:
  - Creates or removes connected device from Nautobot
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
    - name: Create connected_device within Nautobot with only required information
      networktocode.nautobot.connected_device:
        url: http://nautobot.local
        token: thisIsMyToken
        state: present

    - name: Delete connected_device within nautobot
      networktocode.nautobot.connected_device:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
connected_device:
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
    NB_CONNECTED_DEVICE,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    connected_device = NautobotDcimModule(module, NB_CONNECTED_DEVICE)
    connected_device.run()


if __name__ == "__main__":  # pragma: no cover
    main()
