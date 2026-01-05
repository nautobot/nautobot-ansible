#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: unique_rule
short_description: Create, update or delete unique rules in Nautobot
description:
  - Creates, updates or removes unique rules from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "6.1.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the unique rule
      - Required if I(state=present) and the unique rule does not exist yet
    required: false
    type: str
  content_type:
    description:
      - The content type of the unique rule (e.g., dcim.device, ipam.prefix, etc.)
      - Required if I(state=present) and the unique rule does not exist yet
    required: false
    type: str
  field:
    description:
      - The field to apply the unique rule to (e.g., name, description, etc.)
      - Required if I(state=present) and the unique rule does not exist yet
    required: false
    type: str
  enabled:
    description:
      - Whether the unique rule is enabled or disabled
    required: false
    type: bool
  error_message:
    description:
      - The error message to display if the unique rule is violated
    required: false
    type: str
  max_instances:
    description:
      - The maximum number of unique instances of the field within the content type
    required: false
    type: int
"""

EXAMPLES = r"""
- name: Create a unique rule
  networktocode.nautobot.unique_rule:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Unique Rule"
    content_type: "dcim.device"
    field: "serial"
    enabled: true
    error_message: "Asset tag must be unique"
    max_instances: 2
    state: present

- name: Delete a unique rule
  networktocode.nautobot.unique_rule:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Unique Rule"
    state: absent

- name: Delete a unique rule by id
  networktocode.nautobot.unique_rule:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
unique_rule:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.data_validation import (
    NB_UNIQUE_RULES,
    NautobotDataValidationModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            content_type=dict(required=False, type="str"),
            field=dict(required=False, type="str"),
            enabled=dict(required=False, type="bool"),
            error_message=dict(required=False, type="str"),
            max_instances=dict(required=False, type="int"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    unique_rule = NautobotDataValidationModule(module, NB_UNIQUE_RULES)
    unique_rule.run()


if __name__ == "__main__":  # pragma: no cover
    main()
