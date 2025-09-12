#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: virtual_chassis
short_description: Creates or removes virtual chassis from Nautobot
description:
  - Creates or removes virtual chassis from Nautobot
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
  domain:
    required: false
    type: str
  master:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create virtual_chassis within Nautobot with only required information
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual_Chassis
        state: present

    - name: Delete virtual_chassis within nautobot
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual_Chassis
        state: absent
"""

RETURN = r"""
virtual_chassis:
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
    NB_VIRTUAL_CHASSIS,
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
            domain=dict(required=False, type="str"),
            master=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    virtual_chassis = NautobotDcimModule(module, NB_VIRTUAL_CHASSIS)
    virtual_chassis.run()


if __name__ == "__main__":  # pragma: no cover
    main()
