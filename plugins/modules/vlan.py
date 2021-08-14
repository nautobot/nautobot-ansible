#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

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
requirements:
  - pynautobot
version_added: "1.0.0"
options:
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
  site:
    description:
      - The site the VLAN will be associated to
    required: false
    type: raw
  vlan_group:
    description:
      - The VLAN group the VLAN will be associated to
    required: false
    type: raw
  vid:
    description:
      - The VLAN ID
    required: false
    type: int
  name:
    description:
      - The name of the vlan
    required: true
    type: str
  tenant:
    description:
      - The tenant that the vlan will be assigned to
    required: false
    type: raw
  status:
    description:
      - The status of the vlan
    required: false
    type: raw
  vlan_role:
    description:
      - The role of the VLAN.
    required: false
    type: raw
  description:
    description:
      - The description of the vlan
    required: false
    type: str
  tags:
    description:
      - Any tags that the vlan may need to be associated with
    required: false
    type: list
    elements: raw
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
    type: dict
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

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
        site: Test Site
        group: Test VLAN Group
        tenant: Test Tenant
        status: Deprecated
        vlan_role: Test VLAN Role
        description: Just a test
        tags:
          - Schnozzberry
        state: present
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_VLANS,
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
            site=dict(required=False, type="raw"),
            vlan_group=dict(required=False, type="raw"),
            vid=dict(required=False, type="int"),
            name=dict(required=True, type="str"),
            tenant=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            vlan_role=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )
    required_if = [
        ("state", "present", ["name", "status"]),
        ("state", "absent", ["name"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    vlan = NautobotIpamModule(module, NB_VLANS)
    vlan.run()


if __name__ == "__main__":  # pragma: no cover
    main()
