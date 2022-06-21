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
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  api_version:
    description:
      - API Version Nautobot REST API
    required: false
    type: str
    version_added: "4.0.1"
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
  slug:
    description:
      - URL-friendly unique shorthand
    required: false
    type: str
    version_added: "3.0.0"
  tags:
    description:
      - Any tags that the tenant may need to be associated with
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
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
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
        group: Very Special Tenants
        description: ABC Incorporated
        comments: '### This tenant is super cool'
        slug: tenant_abc
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
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
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            tenant_group=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
            slug=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    tenant = NautobotTenancyModule(module, NB_TENANTS)
    tenant.run()


if __name__ == "__main__":  # pragma: no cover
    main()
