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
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the vrf
    required: true
    type: str
    version_added: "3.0.0"
  namespace:
    description:
      - namespace that IP address is associated with. VRFs are unique per namespaces.
    required: false
    default: Global
    type: str
    version_added: "5.0.0"
  rd:
    description:
      - The RD of the VRF. Must be quoted to pass as a string.
    required: true
    type: str
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the vrf will be assigned to
    required: false
    type: raw
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
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create vrf within Nautobot with only required information
      networktocode.nautobot.vrf:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VRF
        state: present
        rd: "65000:1"

    - name: Delete vrf within nautobot
      networktocode.nautobot.vrf:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VRF
        state: absent
        rd: "65000:1"

    - name: Create vrf with all information
      networktocode.nautobot.vrf:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VRF
        rd: "65000:1"
        tenant: Test Tenant
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
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
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            namespace=dict(required=False, type="str", default="Global"),
            rd=dict(required=True, type="str"),
            tenant=dict(required=False, type="raw"),
            import_targets=dict(required=False, type="list", elements="str"),
            export_targets=dict(required=False, type="list", elements="str"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vrf = NautobotIpamModule(module, NB_VRFS)
    vrf.run()


if __name__ == "__main__":  # pragma: no cover
    main()
