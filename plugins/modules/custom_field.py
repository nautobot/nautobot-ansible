#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
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
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.1.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  label:
    description:
      - Name of the field as displayed to users
    required: true
    type: str
    version_added: "5.1.0"
  grouping:
    description:
      - Human-readable grouping that this custom field belongs to
    required: false
    type: str
    version_added: "5.1.0"
  key:
    description:
      - Internal name of this field
      - Required if I(state=present) and the custom field does not exist yet
    required: false
    type: str
    version_added: "5.1.0"
  type:
    description:
      - Data type of this field
      - Required if I(state=present) and the custom field does not exist yet
      - I(type=select) and I(type=multi-select) require choices to be defined separately with the I(custom_field_choice) module
    required: false
    choices:
      - text
      - integer
      - boolean
      - date
      - url
      - select
      - multi-select
      - json
      - markdown
    type: str
    version_added: "5.1.0"
  weight:
    description:
      - Position this field should be displayed in
    required: false
    type: int
    version_added: "5.1.0"
  description:
    description:
      - Description of this field
      - Also used as the help text when editing models using this custom field
      - Markdown is supported
    required: false
    type: str
    version_added: "5.1.0"
  required:
    description:
      - Whether or not a value is required for this field when editing models
    required: false
    type: bool
    version_added: "5.1.0"
  default:
    description:
      - Default value for this field when editing models
      - Must be in JSON format
    required: false
    type: raw
    version_added: "5.1.0"
  filter_logic:
    description:
      - Filter logic to apply when filtering models based on this field
      - Only compatible with I(type=text), I(type=url) and I(type=json)
    required: false
    type: str
    choices:
      - disabled
      - loose
      - exact
    version_added: "5.1.0"
  advanced_ui:
    description:
      - Whether or not to display this field in the advanced tab
    required: false
    type: bool
    version_added: "5.1.0"
  content_types:
    description:
      - Content types that this field should be available for
      - Required if I(state=present) and the custom field does not exist yet
    required: false
    type: list
    elements: str
    version_added: "5.1.0"
  validation_minimum:
    description:
      - Minimum value allowed for this field
      - Only compatible with I(type=integer)
    required: false
    type: int
    version_added: "5.1.0"
  validation_maximum:
    description:
      - Maximum value allowed for this field
      - Only compatible with I(type=integer)
    required: false
    type: int
    version_added: "5.1.0"
  validation_regex:
    description:
      - Regular expression that this field must match
      - Only compatible with I(type=text)
    required: false
    type: str
    version_added: "5.1.0"
"""

EXAMPLES = r"""
- name: Create custom field within Nautobot with only required information
  networktocode.nautobot.custom_field:
    url: http://nautobot.local
    token: thisIsMyToken
    label: My Custom Field
    key: my_custom_field
    type: text
    state: present

- name: Create custom field within Nautobot with all information
  networktocode.nautobot.custom_field:
    url: http://nautobot.local
    token: thisIsMyToken
    label: My Custom Field
    grouping: My Grouping
    key: my_custom_field
    type: text
    weight: 100
    description: My Description
    required: true
    default: My Default
    filter_logic: loose
    advanced_ui: true
    content_types:
      - dcim.device
    validation_minimum: 0
    validation_maximum: 100
    validation_regex: ^[a-z]+$
    state: present
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_CUSTOM_FIELDS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """Execute custom field module."""
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            label=dict(required=True, type="str"),
            grouping=dict(required=False, type="str"),
            key=dict(required=False, type="str"),
            type=dict(required=False, choices=["text", "integer", "boolean", "date", "url", "select", "multi-select", "json", "markdown"], type="str"),
            weight=dict(required=False, type="int"),
            description=dict(required=False, type="str"),
            required=dict(required=False, type="bool"),
            default=dict(required=False, type="raw"),
            filter_logic=dict(required=False, choices=["disabled", "loose", "exact"], type="str"),
            advanced_ui=dict(required=False, type="bool"),
            content_types=dict(required=False, type="list", elements="str"),
            validation_minimum=dict(required=False, type="int"),
            validation_maximum=dict(required=False, type="int"),
            validation_regex=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    custom_field = NautobotExtrasModule(module, NB_CUSTOM_FIELDS)
    custom_field.run()


if __name__ == "__main__":  # pragma: no cover
    main()
