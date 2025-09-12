#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: custom_field_choice
short_description: Creates or removes custom field choices from Nautobot
description:
  - Creates or removes custom field choices from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  id:
    required: false
    type: str
  value:
    required: true
    type: str
  weight:
    required: false
    type: int
  custom_field:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create custom_field_choice within Nautobot with only required information
      networktocode.nautobot.custom_field_choice:
        url: http://nautobot.local
        token: thisIsMyToken
        value: "Test value"
        custom_field: None
        state: present

    - name: Delete custom_field_choice within nautobot
      networktocode.nautobot.custom_field_choice:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
custom_field_choice:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_CUSTOM_FIELD_CHOICES,
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
            value=dict(required=True, type="str"),
            weight=dict(required=False, type="int"),
            custom_field=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    custom_field_choice = NautobotExtrasModule(module, NB_CUSTOM_FIELD_CHOICES)
    custom_field_choice.run()


if __name__ == "__main__":  # pragma: no cover
    main()
