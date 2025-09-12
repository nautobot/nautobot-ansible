#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: virtual_device_context
short_description: Creates or removes virtual device contexts from Nautobot
description:
  - Creates or removes virtual device contexts from Nautobot
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
  identifier:
    required: true
    type: int
  description:
    required: false
    type: str
  device:
    required: true
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
  tenant:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create virtual_device_context within Nautobot with only required information
      networktocode.nautobot.virtual_device_context:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual_Device_Context
        identifier: None
        device: None
        status: "Active"
        state: present

    - name: Delete virtual_device_context within nautobot
      networktocode.nautobot.virtual_device_context:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual_Device_Context
        state: absent
"""

RETURN = r"""
virtual_device_context:
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
    NautobotDcimModule,
    NB_VIRTUAL_DEVICE_CONTEXTS,
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
            identifier=dict(required=True, type="int"),
            description=dict(required=False, type="str"),
            device=dict(required=True, type="dict"),
            status=dict(required=True, type="str"),
            role=dict(required=False, type="dict"),
            primary_ip4=dict(required=False, type="dict"),
            primary_ip6=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    virtual_device_context = NautobotDcimModule(module, NB_VIRTUAL_DEVICE_CONTEXTS)
    virtual_device_context.run()


if __name__ == "__main__":  # pragma: no cover
    main()
