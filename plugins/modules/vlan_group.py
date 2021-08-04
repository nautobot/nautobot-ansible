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
module: vlan_group
short_description: Create, update or delete vlans groups within Nautobot
description:
  - Creates, updates or removes vlans groups from Nautobot
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
  data:
    type: dict
    description:
      - Defines the vlan group configuration
    suboptions:
      name:
        description:
          - The name of the vlan group
        required: true
        type: str
      slug:
        description:
          - The slugified version of the name or custom slug.
          - This is auto-generated following Nautobot rules if not provided
        required: false
        type: str
      site:
        description:
          - The site the vlan will be assigned to
        required: false
        type: raw
      description:
        description:
          - The description of the vlan group
        required: false
        type: str
    required: true
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
    - name: Create vlan group within Nautobot with only required information
      networktocode.nautobot.vlan_group:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test vlan group
          site: Test Site
        state: present

    - name: Delete vlan group within nautobot
      networktocode.nautobot.vlan_group:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test vlan group
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotAnsibleModule,
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_VLAN_GROUPS,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(required=True, type="str"),
                    slug=dict(required=False, type="str"),
                    site=dict(required=False, type="raw"),
                    description=dict(required=False, type="str"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    vlan_group = NautobotIpamModule(module, NB_VLAN_GROUPS)
    vlan_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
