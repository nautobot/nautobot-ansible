#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vlan_location
short_description: Create, update or delete Location assignments to VLANs within Nautobot
description:
  - Create, update or delete Location assignments to VLANs within Nautobot
notes:
  - This module requires Nautobot v2.2+
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
version_added: "5.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  vlan:
    description:
      - The VLAN to associate with the location
      - Required if I(state=present) and the vlan to location assignment does not exist yet
    required: false
    type: raw
  location:
    description:
      - The location the VLAN will be associated to
      - Required if I(state=present) and the vlan to location assignment does not exist yet
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Assign Location to VLAN
      networktocode.nautobot.vlan_location:
        url: http://nautobot.local
        token: thisIsMyToken
        vlan: Test VLAN
        location:
          name: My Child Location
          parent: My Parent Location
        state: present

    - name: Unassign Location from VLAN
      networktocode.nautobot.vlan_location:
        url: http://nautobot.local
        token: thisIsMyToken
        vlan: Test VLAN
        location: My Location
        state: absent

    - name: Delete vlan to location assignment by id
      networktocode.nautobot.vlan_location:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
vlan_location_assignments:
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
    NB_VLAN_LOCATIONS,
    NautobotIpamModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            vlan=dict(required=False, type="raw"),
            location=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vlan_location = NautobotIpamModule(module, NB_VLAN_LOCATIONS)
    vlan_location.run()


if __name__ == "__main__":  # pragma: no cover
    main()
