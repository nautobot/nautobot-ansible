#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: min_max_rule
short_description: Create, update or delete min/max rules in Nautobot
description:
  - Creates, updates or removes min/max rules from Nautobot
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
      - The name of the min/max rule
      - Required if I(state=present) and the min/max rule does not exist yet
    required: false
    type: str
  content_type:
    description:
      - The content type of the min/max rule (e.g., dcim.device, ipam.prefix, etc.)
      - Required if I(state=present) and the min/max rule does not exist yet
    required: false
    type: str
  field:
    description:
      - The field to apply the min/max rule to (e.g., name, description, etc.)
      - Required if I(state=present) and the min/max rule does not exist yet
    required: false
    type: str
  enabled:
    description:
      - Whether the min/max rule is enabled or disabled
    required: false
    type: bool
  error_message:
    description:
      - The error message to display if the min/max rule is violated
    required: false
    type: str
  min:
    description:
      - The minimum value for the min/max rule
      - At least one of I(min) or I(max) must be specified when I(state=present) and the min/max rule does not exist yet
    required: false
    type: float
  max:
    description:
      - The maximum value for the min/max rule
      - At least one of I(min) or I(max) must be specified when I(state=present) and the min/max rule does not exist yet
    required: false
    type: float
"""

EXAMPLES = r"""
- name: Create a min/max rule
  networktocode.nautobot.min_max_rule:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Min/Max Rule"
    content_type: "dcim.location"
    field: "asn"
    enabled: true
    error_message: "ASN must be between 1 and 65535"
    min: 1
    max: 65535
    state: present

- name: Delete a min/max rule
  networktocode.nautobot.min_max_rule:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Min/Max Rule"
    state: absent

- name: Delete a min/max rule by id
  networktocode.nautobot.min_max_rule:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
min_max_rule:
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
    NB_MIN_MAX_RULES,
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
            min=dict(required=False, type="float"),
            max=dict(required=False, type="float"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    min_max_rule = NautobotDataValidationModule(module, NB_MIN_MAX_RULES)
    min_max_rule.run()


if __name__ == "__main__":  # pragma: no cover
    main()
