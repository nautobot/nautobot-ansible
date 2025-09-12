#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: config_context_schema
short_description: Creates or removes config context schemas from Nautobot
description:
  - Creates or removes config context schemas from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  owner_content_type:
    required: false
    type: str
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  data_schema:
    required: true
    type: str
  owner_object_id:
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create config_context_schema within Nautobot with only required information
      networktocode.nautobot.config_context_schema:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Config_Context_Schema
        data_schema: None
        state: present

    - name: Delete config_context_schema within nautobot
      networktocode.nautobot.config_context_schema:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Config_Context_Schema
        state: absent
"""

RETURN = r"""
config_context_schema:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_CONFIG_CONTEXT_SCHEMAS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            owner_content_type=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            data_schema=dict(required=True, type="str"),
            owner_object_id=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    config_context_schema = NautobotExtrasModule(module, NB_CONFIG_CONTEXT_SCHEMAS)
    config_context_schema.run()


if __name__ == "__main__":  # pragma: no cover
    main()
