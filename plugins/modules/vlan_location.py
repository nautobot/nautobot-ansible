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
options:
  vlan:
    description:
      - The VLAN to associate with the location
    required: true
    type: raw
  location:
    description:
      - The location the VLAN will be associated to
    required: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_VLAN_LOCATIONS,
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
            vlan=dict(required=True, type="raw"),
            location=dict(required=True, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vlan_location = NautobotIpamModule(module, NB_VLAN_LOCATIONS)
    vlan_location.run()


if __name__ == "__main__":  # pragma: no cover
    main()
