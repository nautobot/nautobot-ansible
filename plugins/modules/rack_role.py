#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rack_role
short_description: Create, update or delete racks roles within Nautobot
description:
  - Creates, updates or removes racks roles from Nautobot
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
      - The name of the rack role
    required: true
    type: str
    version_added: "3.0.0"
  slug:
    description:
      - The slugified version of the name or custom slug.
      - This is auto-generated following Nautobot rules if not provided
    required: false
    type: str
    version_added: "3.0.0"
  color:
    description:
      - Hexidecimal code for a color, ex. FFFFFF
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create rack role within Nautobot with only required information
      networktocode.nautobot.rack_role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test rack role
        color: FFFFFF
        state: present

    - name: Delete rack role within nautobot
      networktocode.nautobot.rack_role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rack role
        state: absent
"""

RETURN = r"""
rack_role:
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
    NB_RACK_ROLES,
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
            slug=dict(required=False, type="str"),
            color=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rack_role = NautobotDcimModule(module, NB_RACK_ROLES)
    rack_role.run()


if __name__ == "__main__":  # pragma: no cover
    main()
