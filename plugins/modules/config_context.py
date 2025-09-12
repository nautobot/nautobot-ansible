#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: config_context
short_description: Creates or removes config contexts from Nautobot
description:
  - Creates or removes config contexts from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
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
  owner_object_id:
    required: false
    type: str
  weight:
    required: false
    type: int
  description:
    required: false
    type: str
  is_active:
    required: false
    type: bool
  data:
    required: true
    type: str
  config_context_schema:
    required: false
    type: dict
  locations:
    required: false
    type: list
  roles:
    required: false
    type: list
  device_types:
    required: false
    type: list
  device_redundancy_groups:
    required: false
    type: list
  platforms:
    required: false
    type: list
  cluster_groups:
    required: false
    type: list
  clusters:
    required: false
    type: list
  tenant_groups:
    required: false
    type: list
  tenants:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create config context within Nautobot with only required information
      networktocode.nautobot.config_context:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Config Context
        data: None
        state: present

    - name: Delete config_context within nautobot
      networktocode.nautobot.config_context:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Config_Context
        state: absent
"""

RETURN = r"""
config_context:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NB_CONFIG_CONTEXTS,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC, TAGS_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            owner_content_type=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            owner_object_id=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
            description=dict(required=False, type="str"),
            is_active=dict(required=False, type="bool"),
            data=dict(required=True, type="str"),
            config_context_schema=dict(required=False, type="dict"),
            locations=dict(required=False, type="list"),
            roles=dict(required=False, type="list"),
            device_types=dict(required=False, type="list"),
            device_redundancy_groups=dict(required=False, type="list"),
            platforms=dict(required=False, type="list"),
            cluster_groups=dict(required=False, type="list"),
            clusters=dict(required=False, type="list"),
            tenant_groups=dict(required=False, type="list"),
            tenants=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    config_context = NautobotExtrasModule(module, NB_CONFIG_CONTEXTS)
    config_context.run()


if __name__ == "__main__":  # pragma: no cover
    main()
