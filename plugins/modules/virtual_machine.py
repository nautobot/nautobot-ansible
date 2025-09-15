#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: virtual_machine
short_description: Creates or removes virtual machines from Nautobot
description:
  - Creates or removes virtual machines from Nautobot
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
  local_config_context_data:
    required: false
    type: str
  local_config_context_data_owner_object_id:
    required: false
    type: str
  name:
    required: true
    type: str
  vcpus:
    required: false
    type: int
  memory:
    required: false
    type: int
  disk:
    required: false
    type: int
  comments:
    required: false
    type: str
  local_config_context_schema:
    required: false
    type: dict
  local_config_context_data_owner_content_type:
    required: false
    type: dict
  cluster:
    required: true
    type: dict
  tenant:
    required: false
    type: dict
  platform:
    required: false
    type: dict
  status:
    required: true
    type: str
  role:
    required: false
    type: dict
  primary_ip4:
    required: false
    type: dict
  primary_ip6:
    required: false
    type: dict
  software_version:
    required: false
    type: dict
  software_image_files:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create virtual machine within Nautobot with only required information
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        cluster: None
        status: "Active"
        state: present

    - name: Delete virtual_machine within nautobot
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        state: absent
"""

RETURN = r"""
virtual_machine:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.virtualization import (
    NB_VIRTUAL_MACHINES,
    NautobotVirtualizationModule,
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
            local_config_context_data=dict(required=False, type="str"),
            local_config_context_data_owner_object_id=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            vcpus=dict(required=False, type="int"),
            memory=dict(required=False, type="int"),
            disk=dict(required=False, type="int"),
            comments=dict(required=False, type="str"),
            local_config_context_schema=dict(required=False, type="dict"),
            local_config_context_data_owner_content_type=dict(required=False, type="dict"),
            cluster=dict(required=True, type="dict"),
            tenant=dict(required=False, type="dict"),
            platform=dict(required=False, type="dict"),
            status=dict(required=True, type="str"),
            role=dict(required=False, type="dict"),
            primary_ip4=dict(required=False, type="dict"),
            primary_ip6=dict(required=False, type="dict"),
            software_version=dict(required=False, type="dict"),
            software_image_files=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    virtual_machine = NautobotVirtualizationModule(module, NB_VIRTUAL_MACHINES)
    virtual_machine.run()


if __name__ == "__main__":  # pragma: no cover
    main()
