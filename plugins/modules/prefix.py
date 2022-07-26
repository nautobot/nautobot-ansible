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
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  api_version:
    description:
      - API Version Nautobot REST API
    required: false
    type: str
    version_added: "4.1.0"
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  family:
    description:
      - Specifies which address family the prefix prefix belongs to
    required: false
    type: int
    version_added: "3.0.0"
  prefix:
    description:
      - Required if state is C(present) and first_available is False. Will allocate or free this prefix.
    required: false
    type: raw
    version_added: "3.0.0"
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
  site:
    description:
      - Site that prefix is associated with
    required: false
    type: raw
    version_added: "3.0.0"
  vrf:
    description:
      - VRF that prefix is associated with
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
  prefix_role:
    description:
      - The role of the prefix
    required: false
    type: raw
    version_added: "3.0.0"
  is_pool:
    description:
      - All IP Addresses within this prefix are considered usable
    required: false
    type: bool
    version_added: "3.0.0"
  description:
    description:
      - The description of the prefix
    required: false
    type: str
    version_added: "3.0.0"
  tags:
    description:
      - Any tags that the prefix may need to be associated with
    required: false
    type: list
    elements: raw
    version_added: "3.0.0"
  custom_fields:
    description:
      - Must exist in Nautobot and in key/value format
    required: false
    type: dict
    version_added: "3.0.0"
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  first_available:
    description:
      - If C(yes) and state C(present), if an parent is given, it will get the
        first available prefix of the given prefix_length inside the given parent (and
        vrf, if given).
        Unused with state C(absent).
    default: false
    type: bool
    version_added: "3.0.0"
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
    version_added: "3.0.0"
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot prefix module"
  connection: local
  hosts: localhost
  gather_facts: False

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
        family: 4
        prefix: 10.156.32.0/19
        site: Test Site
        vrf: Test VRF
        tenant: Test Tenant
        vlan:
          name: Test VLAN
          site: Test Site
          tenant: Test Tenant
          vlan_group: Test Vlan Group
        status: Reserved
        prefix_role: Network of care
        description: Test description
        is_pool: true
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
        first_available: yes

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
        first_available: yes

    - name: Get a new /24 inside 10.157.0.0/19 within Nautobot with additional values
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 10.157.0.0/19
        prefix_length: 24
        vrf: Test VRF
        site: Test Site
        state: present
        first_available: yes
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


from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
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
    argument_spec.update(
        dict(
            family=dict(required=False, type="int"),
            prefix=dict(required=False, type="raw"),
            parent=dict(required=False, type="raw"),
            prefix_length=dict(required=False, type="int"),
            site=dict(required=False, type="raw"),
            vrf=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            vlan=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            prefix_role=dict(required=False, type="raw"),
            is_pool=dict(required=False, type="bool"),
            description=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
            first_available=dict(required=False, type="bool", default=False),
        )
    )

    required_if = [
        ("state", "present", ["prefix", "parent", "status"], True),
        ("state", "absent", ["prefix"]),
        ("first_available", "yes", ["parent"]),
    ]

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    prefix = NautobotIpamModule(module, NB_PREFIXES, remove_keys=["first_available"])
    prefix.run()


if __name__ == "__main__":  # pragma: no cover
    main()
