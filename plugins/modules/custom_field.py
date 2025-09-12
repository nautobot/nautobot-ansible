#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: custom_field
short_description: Creates or removes custom fields from Nautobot
description:
  - Creates or removes custom fields from Nautobot
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
  content_types:
    required: true
    type: list
  label:
    required: true
    type: str
  grouping:
    required: false
    type: str
  type:
    required: false
    type: str
  key:
    required: false
    type: str
  description:
    required: false
    type: str
  required:
    required: false
    type: bool
  filter_logic:
    required: false
    type: str
  default:
    required: false
    type: str
  weight:
    required: false
    type: int
  validation_minimum:
    required: false
    type: int
  validation_maximum:
    required: false
    type: int
  validation_regex:
    required: false
    type: str
  advanced_ui:
    required: false
    type: bool
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create custom field within Nautobot with only required information
      networktocode.nautobot.custom_field:
        url: http://nautobot.local
        token: thisIsMyToken
        content_types: None
        label: "Test Label"
        state: present

    - name: Delete custom_field within nautobot
      networktocode.nautobot.custom_field:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
custom_field:
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
    NB_CUSTOM_FIELDS,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            content_types=dict(required=True, type="list"),
            label=dict(required=True, type="str"),
            grouping=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            key=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            required=dict(required=False, type="bool"),
            filter_logic=dict(required=False, type="str"),
            default=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
            validation_minimum=dict(required=False, type="int"),
            validation_maximum=dict(required=False, type="int"),
            validation_regex=dict(required=False, type="str"),
            advanced_ui=dict(required=False, type="bool"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    custom_field = NautobotExtrasModule(module, NB_CUSTOM_FIELDS)
    custom_field.run()


if __name__ == "__main__":  # pragma: no cover
    main()
