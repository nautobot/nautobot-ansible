#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: external_integration
short_description: Creates or removes external integrations from Nautobot
description:
  - Creates or removes external integrations from Nautobot
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
  remote_url:
    required: true
    type: str
  verify_ssl:
    required: false
    type: bool
  timeout:
    required: false
    type: int
  extra_config:
    required: false
    type: str
  http_method:
    required: false
    type: str
    choices:
      - "GET"
      - "POST"
      - "PUT"
      - "PATCH"
      - "DELETE"
  headers:
    required: false
    type: str
  ca_file_path:
    required: false
    type: str
  secrets_group:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create external_integration within Nautobot with only required information
      networktocode.nautobot.external_integration:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test External_Integration
        remote_url: "Test remote_url"
        state: present

    - name: Delete external_integration within nautobot
      networktocode.nautobot.external_integration:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test External_Integration
        state: absent
"""

RETURN = r"""
external_integration:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_EXTERNAL_INTEGRATIONS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


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
            remote_url=dict(required=True, type="str"),
            verify_ssl=dict(required=False, type="bool"),
            timeout=dict(required=False, type="int"),
            extra_config=dict(required=False, type="str"),
            http_method=dict(
                required=False,
                type="str",
                choices=[
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                ],
            ),
            headers=dict(required=False, type="str"),
            ca_file_path=dict(required=False, type="str"),
            secrets_group=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    external_integration = NautobotExtrasModule(module, NB_EXTERNAL_INTEGRATIONS)
    external_integration.run()


if __name__ == "__main__":  # pragma: no cover
    main()
