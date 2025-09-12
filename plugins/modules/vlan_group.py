#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vlan_group
short_description: Create, update or delete vlans groups within Nautobot
description:
  - Creates, updates or removes vlans groups from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the vlan group
      - Required if I(state=present) and the vlan group does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  location:
    description:
      - The location the vlan will be assigned to
    required: false
    type: raw
    version_added: "5.0.0"
  description:
    description:
      - The description of the vlan group
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create vlan group within Nautobot with only required information
      networktocode.nautobot.vlan_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test vlan group
        location:
          name: My Location
          parent: Parent Location
        state: present

    - name: Delete vlan group within nautobot
      networktocode.nautobot.vlan_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test vlan group
        state: absent

    - name: Delete vlan group by id
      networktocode.nautobot.vlan_group:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
vlan_group:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NB_VLAN_GROUPS,
    NautobotIpamModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            location=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vlan_group = NautobotIpamModule(module, NB_VLAN_GROUPS)
    vlan_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
