#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vlan
short_description: Create, update or delete vlans within Nautobot
description:
  - Creates, updates or removes vlans from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  location:
    description:
      - The single location the VLAN will be associated to
      - If you want to associate multiple locations, use the C(vlan_location) module
      - Using this parameter will override the C(api_version) option to C(2.0)
    required: false
    type: raw
    version_added: "3.0.0"
  vlan_group:
    description:
      - The VLAN group the VLAN will be associated to
    required: false
    type: raw
    version_added: "3.0.0"
  vid:
    description:
      - The VLAN ID
    required: false
    type: int
    version_added: "3.0.0"
  name:
    description:
      - The name of the vlan
      - Required if I(state=present) and the vlan does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the vlan will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  status:
    description:
      - The status of the vlan
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  role:
    description:
      - The role of the VLAN.
    required: false
    type: raw
    version_added: "3.0.0"
  description:
    description:
      - The description of the vlan
    required: false
    type: str
    version_added: "3.0.0"
  group:
    description:
      - The group of the VLAN.
    required: false
    type: raw
    version_added: "5.10.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create vlan within Nautobot with only required information
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VLAN
        vid: 400
        status: active
        state: present

    - name: Delete vlan within nautobot
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VLAN
        vid: 400
        status: active
        state: absent

    - name: Create vlan with all information
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VLAN
        vid: 400
        location:
          name: My Location
          parent: Parent Location
        group: Test VLAN Group
        tenant: Test Tenant
        status: Deprecated
        role: Test VLAN Role
        description: Just a test
        tags:
          - Schnozzberry
        state: present

    - name: Delete vlan by id
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
vlan:
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
    NB_VLANS,
    NautobotIpamModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            location=dict(required=False, type="raw"),
            vlan_group=dict(required=False, type="raw"),
            vid=dict(required=False, type="int"),
            name=dict(required=False, type="str"),
            tenant=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            group=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vlan = NautobotIpamModule(module, NB_VLANS)
    vlan.run()


if __name__ == "__main__":  # pragma: no cover
    main()
