#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rack_group
short_description: Create, update or delete racks groups within Nautobot
description:
  - Creates, updates or removes racks groups from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  description:
    description:
      - The description of the rack group
    required: false
    type: str
    version_added: "3.0.0"
  name:
    description:
      - The name of the rack group
    required: true
    type: str
    version_added: "3.0.0"
  location:
    description:
      - Required if I(state=present) and the rack does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  parent_rack_group:
    aliases:
      - parent
    description:
      - The parent rack-group the rack group will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create rack group within Nautobot with only required information
      networktocode.nautobot.rack_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test rack group
        location: My Location
        state: present

    - name: Delete rack group within nautobot
      networktocode.nautobot.rack_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rack group
        location:
          name: My Location
          parent: Parent Location
        state: absent
"""

RETURN = r"""
rack_group:
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
    NB_RACK_GROUPS,
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
            description=dict(required=False, type="str"),
            location=dict(required=False, type="raw"),
            parent_rack_group=dict(required=False, type="raw", aliases=["parent"]),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rack_group = NautobotDcimModule(module, NB_RACK_GROUPS)
    rack_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
