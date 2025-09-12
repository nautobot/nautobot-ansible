#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: prefix_location_assignment
short_description: Creates or removes prefix location assignments from Nautobot
description:
  - Creates or removes prefix location assignments from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  id:
    required: false
    type: str
  prefix:
    required: true
    type: dict
  location:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create prefix_location_assignment within Nautobot with only required information
      networktocode.nautobot.prefix_location_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: None
        location: None
        state: present

    - name: Delete prefix_location_assignment within nautobot
      networktocode.nautobot.prefix_location_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
prefix_location_assignment:
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
    NB_PREFIX_LOCATION_ASSIGNMENTS,
    NautobotIpamModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            prefix=dict(required=True, type="dict"),
            location=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    prefix_location_assignment = NautobotIpamModule(module, NB_PREFIX_LOCATION_ASSIGNMENTS)
    prefix_location_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
