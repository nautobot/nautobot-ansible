#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: computed_field
short_description: Creates or removes computed fields from Nautobot
description:
  - Creates or removes computed fields from Nautobot
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
  content_type:
    required: true
    type: str
  key:
    required: false
    type: str
  grouping:
    required: false
    type: str
  label:
    required: true
    type: str
  description:
    required: false
    type: str
  template:
    required: true
    type: str
  fallback_value:
    required: false
    type: str
  weight:
    required: false
    type: int
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
    - name: Create computed field within Nautobot with only required information
      networktocode.nautobot.computed_field:
        url: http://nautobot.local
        token: thisIsMyToken
        content_type: "Test content_type"
        label: "Test label"
        template: "Test template"
        state: present

    - name: Delete computed_field within nautobot
      networktocode.nautobot.computed_field:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
computed_field:
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
    NB_COMPUTED_FIELDS,
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
            content_type=dict(required=True, type="str"),
            key=dict(required=False, type="str"),
            grouping=dict(required=False, type="str"),
            label=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            template=dict(required=True, type="str"),
            fallback_value=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
            advanced_ui=dict(required=False, type="bool"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    computed_field = NautobotExtrasModule(module, NB_COMPUTED_FIELDS)
    computed_field.run()


if __name__ == "__main__":  # pragma: no cover
    main()
