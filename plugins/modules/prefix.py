#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: prefix
short_description: Creates or removes prefixes from Nautobot
description:
  - Creates or removes prefixes from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
  - Anthony Ruhier (@Anthony25)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  ip_version:
    description:
      - Specifies which address version the prefix prefix belongs to
    required: false
    type: int
    version_added: "5.0.0"
  prefix:
    description:
      - Required if state is C(present) and first_available is False. Will allocate or free this prefix.
    required: false
    type: raw
    version_added: "3.0.0"
  namespace:
    description:
      - |
        namespace that IP address is associated with. IPs are unique per namespaces.
    required: false
    default: Global
    type: str
    version_added: "5.0.0"
  parent:
    description:
      - Required if state is C(present) and first_available is C(yes). Will get a new available prefix in this parent prefix.
    required: false
    type: raw
    version_added: "3.0.0"
  prefix_length:
    description:
      - |
        Required ONLY if state is C(present) and first_available is C(yes).
        Will get a new available prefix of the given prefix_length in this parent prefix.
    required: false
    type: int
    version_added: "3.0.0"
  location:
    description:
      - The single location the prefix will be associated to
      - If you want to associate multiple locations, use the C(prefix_location) module
      - Using this parameter will override the C(api_version) option to C(2.0)
    required: false
    type: raw
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the prefix will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  vlan:
    description:
      - The VLAN the prefix will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  status:
    description:
      - The status of the prefix
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  role:
    description:
      - The role of the prefix
    required: false
    type: raw
    version_added: "3.0.0"
  type:
    description:
     - Prefix type
    choices:
      - Container
      - Network
      - Pool
    required: false
    type: str
    version_added: "5.0.0"
  description:
    description:
      - The description of the prefix
    required: false
    type: str
    version_added: "3.0.0"
  first_available:
    description:
      - If C(yes) and state C(present), if an parent is given, it will get the
        first available prefix of the given prefix_length inside the given parent (and
        namespace, if given).
        Unused with state C(absent).
    default: false
    type: bool
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot prefix module"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create prefix within Nautobot with only required information
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 10.156.0.0/19
        status: active
        state: present

    - name: Delete prefix within nautobot
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 10.156.0.0/19
        state: absent

    - name: Create prefix with several specified options
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 10.156.32.0/19
        location: My Location
        tenant: Test Tenant
        vlan:
          name: Test VLAN
          location: My Location
          tenant: Test Tenant
          vlan_group: Test Vlan Group
        status: Reserved
        role: Network of care
        description: Test description
        type: Pool
        tags:
          - Schnozzberry
        state: present

    - name: Get a new /24 inside 10.156.0.0/19 within Nautobot - Parent doesn't exist
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 10.156.0.0/19
        prefix_length: 24
        state: present
        first_available: true

    - name: Create prefix within Nautobot with only required information
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 10.156.0.0/19
        state: present

    - name: Get a new /24 inside 10.156.0.0/19 within Nautobot
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 10.156.0.0/19
        prefix_length: 24
        state: present
        first_available: true

    - name: Get a new /24 inside 10.157.0.0/19 within Nautobot with additional values
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 10.157.0.0/19
        prefix_length: 24
        location:
          name: My Location
          parent: Parent Location
        state: present
        first_available: true
"""

RETURN = r"""
prefix:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""


from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_PREFIXES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            ip_version=dict(required=False, type="int"),
            prefix=dict(required=False, type="raw"),
            parent=dict(required=False, type="raw"),
            prefix_length=dict(required=False, type="int"),
            location=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            vlan=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            type=dict(
                required=False,
                type="str",
                choices=["Container", "Network", "Pool"],
            ),
            description=dict(required=False, type="str"),
            namespace=dict(required=False, type="str", default="Global"),
            first_available=dict(required=False, type="bool", default=False),
        )
    )

    required_if = [
        ("state", "absent", ["prefix"]),
        ("first_available", "yes", ["parent"]),
    ]

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    prefix = NautobotIpamModule(module, NB_PREFIXES, remove_keys=["first_available"])
    prefix.run()


if __name__ == "__main__":  # pragma: no cover
    main()
