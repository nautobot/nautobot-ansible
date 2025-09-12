#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: relationship
short_description: Creates or removes relationships from Nautobot
description:
  - Creates or removes relationships from Nautobot
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
  source_type:
    required: true
    type: str
  destination_type:
    required: true
    type: str
  label:
    required: true
    type: str
  key:
    required: false
    type: str
  description:
    required: false
    type: str
  type:
    required: false
    type: str
  required_on:
    required: false
    type: str
    choices:
      - "source"
      - "destination"
  source_label:
    required: false
    type: str
  source_hidden:
    required: false
    type: bool
  source_filter:
    required: false
    type: str
  destination_label:
    required: false
    type: str
  destination_hidden:
    required: false
    type: bool
  destination_filter:
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
  gather_facts: False

  tasks:
    - name: Create relationship within Nautobot with only required information
      networktocode.nautobot.relationship:
        url: http://nautobot.local
        token: thisIsMyToken
        source_type: "Test source_type"
        destination_type: "Test destination_type"
        label: "Test label"
        state: present

    - name: Delete relationship within nautobot
      networktocode.nautobot.relationship:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
relationship:
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
    NB_RELATIONSHIPS,
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
            source_type=dict(required=True, type="str"),
            destination_type=dict(required=True, type="str"),
            label=dict(required=True, type="str"),
            key=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            required_on=dict(
                required=False,
                type="str",
                choices=[
                    "source",
                    "destination",
                ],
            ),
            source_label=dict(required=False, type="str"),
            source_hidden=dict(required=False, type="bool"),
            source_filter=dict(required=False, type="str"),
            destination_label=dict(required=False, type="str"),
            destination_hidden=dict(required=False, type="bool"),
            destination_filter=dict(required=False, type="str"),
            advanced_ui=dict(required=False, type="bool"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    relationship = NautobotExtrasModule(module, NB_RELATIONSHIPS)
    relationship.run()


if __name__ == "__main__":  # pragma: no cover
    main()
