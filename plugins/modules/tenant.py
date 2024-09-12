#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Amy Liebowitz (@amylieb)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: tenant
short_description: Creates or removes tenants from Nautobot
description:
  - Creates or removes tenants from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Amy Liebowitz (@amylieb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - Name of the tenant to be created
    required: true
    type: str
    version_added: "3.0.0"
  tenant_group:
    description:
      - Tenant group this tenant should be in
    required: false
    type: raw
    version_added: "3.0.0"
  description:
    description:
      - The description of the tenant
    required: false
    type: str
    version_added: "3.0.0"
  comments:
    description:
      - Comments for the tenant. This can be markdown syntax
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create tenant within Nautobot with only required information
      networktocode.nautobot.tenant:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant ABC
        state: present

    - name: Delete tenant within nautobot
      networktocode.nautobot.tenant:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant ABC
        state: absent

    - name: Create tenant with all parameters
      networktocode.nautobot.tenant:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant ABC
        tenant_group: Very Special Tenants
        description: ABC Incorporated
        comments: '### This tenant is super cool'
        tags:
          - tagA
          - tagB
          - tagC
        state: present
"""

RETURN = r"""
tenant:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.tenancy import (
    NautobotTenancyModule,
    NB_TENANTS,
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
            tenant_group=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    tenant = NautobotTenancyModule(module, NB_TENANTS)
    tenant.run()


if __name__ == "__main__":  # pragma: no cover
    main()
