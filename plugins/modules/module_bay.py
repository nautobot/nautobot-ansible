#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: module_bay
short_description: Creates or removes module bays from Nautobot
description:
  - Creates or removes module bays from Nautobot
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
  requires_first_party_modules:
    required: false
    type: bool
  name:
    required: true
    type: str
  position:
    required: false
    type: str
  label:
    required: false
    type: str
  description:
    required: false
    type: str
  parent_device:
    required: false
    type: dict
  parent_module:
    required: false
    type: dict
  module_family:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create module bay within Nautobot with only required information
      networktocode.nautobot.module_bay:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Module Bay
        state: present

    - name: Delete module_bay within nautobot
      networktocode.nautobot.module_bay:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Module Bay
        state: absent
"""

RETURN = r"""
module_bay:
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
    NB_MODULE_BAYS,
    NautobotDcimModule,
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
            requires_first_party_modules=dict(required=False, type="bool"),
            name=dict(required=True, type="str"),
            position=dict(required=False, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            parent_device=dict(required=False, type="dict"),
            parent_module=dict(required=False, type="dict"),
            module_family=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    module_bay = NautobotDcimModule(module, NB_MODULE_BAYS)
    module_bay.run()


if __name__ == "__main__":  # pragma: no cover
    main()
