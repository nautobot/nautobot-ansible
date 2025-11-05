#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: tenant_group
short_description: Creates or removes tenant groups from Nautobot
description:
  - Creates or removes tenant groups from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - Name of the tenant group to be created
      - Required if I(state=present) and the tenant group does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - The description of the tenant
    required: false
    type: str
    version_added: "3.0.0"
  parent_tenant_group:
    aliases:
      - parent
    description:
      - Name of the parent tenant group
    required: false
    type: raw
    version_added: "3.1.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot tenant group module"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create tenant within Nautobot with only required information
      networktocode.nautobot.tenant_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant Group ABC
        state: present

    - name: Delete tenant within Nautobot
      networktocode.nautobot.tenant_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant ABC
        state: absent

    - name: Update tenant within Nautobot with a parent tenant group
      networktocode.nautobot.tenant_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant Group ABC
        parent: Customer Tenants
        state: present

    - name: Delete tenant group by id
      networktocode.nautobot.tenant_group:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
tenant_group:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.tenancy import (
    NB_TENANT_GROUPS,
    NautobotTenancyModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            parent_tenant_group=dict(required=False, type="raw", aliases=["parent"]),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    tenant_group = NautobotTenancyModule(module, NB_TENANT_GROUPS)
    tenant_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
