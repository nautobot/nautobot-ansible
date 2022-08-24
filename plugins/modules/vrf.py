#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vrf
short_description: Create, update or delete vrfs within Nautobot
description:
  - Creates, updates or removes vrfs from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
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
  name:
    description:
      - The name of the vrf
    required: true
    type: str
    version_added: "3.0.0"
  rd:
    description:
      - The RD of the VRF. Must be quoted to pass as a string.
    required: false
    type: str
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the vrf will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  enforce_unique:
    description:
      - Prevent duplicate prefixes/IP addresses within this VRF
    required: false
    type: bool
    version_added: "3.0.0"
  import_targets:
    description:
      - Import targets tied to VRF
    required: false
    type: list
    elements: str
    version_added: "3.0.0"
  export_targets:
    description:
      - Export targets tied to VRF
    required: false
    type: list
    elements: str
    version_added: "3.0.0"
  description:
    description:
      - The description of the vrf
    required: false
    type: str
    version_added: "3.0.0"
  tags:
    description:
      - Any tags that the vrf may need to be associated with
    required: false
    type: list
    elements: raw
    version_added: "3.0.0"
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
    type: dict
    version_added: "3.0.0"
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
    version_added: "3.0.0"
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
    - name: Create vrf within Nautobot with only required information
      networktocode.nautobot.vrf:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VRF
        state: present

    - name: Delete vrf within nautobot
      networktocode.nautobot.vrf:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VRF
        state: absent

    - name: Create vrf with all information
      networktocode.nautobot.vrf:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VRF
        rd: "65000:1"
        tenant: Test Tenant
        enforce_unique: true
        import_targets:
          - "65000:65001"
        export_targets:
          - "65000:65001"
        description: VRF description
        tags:
          - Schnozzberry
        state: present
"""

RETURN = r"""
vrf:
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
    NB_VRFS,
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
            rd=dict(required=False, type="str"),
            tenant=dict(required=False, type="raw"),
            enforce_unique=dict(required=False, type="bool"),
            import_targets=dict(required=False, type="list", elements="str"),
            export_targets=dict(required=False, type="list", elements="str"),
            description=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vrf = NautobotIpamModule(module, NB_VRFS)
    vrf.run()


if __name__ == "__main__":  # pragma: no cover
    main()
