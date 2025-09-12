#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vrf
short_description: Creates or removes vrfs from Nautobot
description:
  - Creates or removes vrfs from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  rd:
    required: true
    type: str
  description:
    required: false
    type: str
  status:
    required: false
    type: str
  namespace:
    required: false
    type: dict
  tenant:
    required: false
    type: dict
  import_targets:
    required: false
    type: list
  export_targets:
    required: false
    type: list
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
        name: Test Vrf
        rd: "Test rd"
        state: present

    - name: Delete vrf within nautobot
      networktocode.nautobot.vrf:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Vrf
        state: absent
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

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_VRFS,
    NautobotIpamModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            rd=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            status=dict(required=False, type="str"),
            namespace=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
            import_targets=dict(required=False, type="list"),
            export_targets=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vrf = NautobotIpamModule(module, NB_VRFS)
    vrf.run()


if __name__ == "__main__":  # pragma: no cover
    main()
