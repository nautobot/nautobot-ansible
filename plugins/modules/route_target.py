#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Pavel Korovin (@pkorovin) <p@tristero.se>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: route_target
short_description: Creates or removes route targets from Nautobot
description:
  - Creates or removes route targets from Nautobot
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
      - Route target name
    required: true
    type: str
  tenant:
    description:
      - The tenant that the route target will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  description:
    description:
      - Tag description
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test route target creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create Route Targets
      networktocode.nautobot.route_target:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "{{ item.name }}"
        tenant: "Test Tenant"
        tags:
          - Schnozzberry
      loop:
        - { name: "65000:65001", description: "management" }
        - { name: "65000:65002", description: "tunnel" }

    - name: Update Description on Route Targets
      networktocode.nautobot.route_target:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "{{ item.name }}"
        tenant: "Test Tenant"
        description: "{{ item.description }}"
        tags:
          - Schnozzberry
      loop:
        - { name: "65000:65001", description: "management" }
        - { name: "65000:65002", description: "tunnel" }

    - name: Delete Route Targets
      networktocode.nautobot.route_target:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "{{ item }}"
        state: absent
      loop:
        - "65000:65001"
        - "65000:65002"
"""

RETURN = r"""
route_target:
  description: Serialized object as created/existent/updated/deleted within Nautobot
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NB_ROUTE_TARGETS,
    NautobotIpamModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            tenant=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    route_target = NautobotIpamModule(module, NB_ROUTE_TARGETS)
    route_target.run()


if __name__ == "__main__":  # pragma: no cover
    main()
