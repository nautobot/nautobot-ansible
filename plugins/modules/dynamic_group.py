#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dynamic_group
short_description: Creates or removes dynamic groups from Nautobot
description:
  - Creates or removes dynamic groups from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
requirements:
  - pynautobot
version_added: "5.5.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the dynamic group
    required: true
    type: str
  description:
    description:
      - The description of the dynamic group
    required: false
    type: str
  group_type:
    description:
      - Required if I(state=present) and the dynamic group does not exist yet
    choices: [ dynamic-filter, dynamic-set, static ]
    required: false
    type: str
  content_type:
    description:
      - Required if I(state=present) and the dynamic group does not exist yet
      - The app_label.model for the objects in the group
    required: false
    type: str
  tenant:
    description:
      - The tenant that the dynamic group will be assigned to
    required: false
    type: raw
  filter:
    description:
      - A dictionary of filter parameters defining membership of this group
    required: false
    type: dict
"""

EXAMPLES = r"""
---
- name: Create a dynamic group
  networktocode.nautobot.dynamic_group:
    url: http://nautobot.local
    token: thisIsMyToken
    name: TestFilterGroup
    group_type: dynamic-filter
    content_type: dcim.device
    filter:
      location:
        - "Child-Child Test Location"
    state: present

- name: Delete a dynamic group
  networktocode.nautobot.dynamic_group:
    url: http://nautobot.local
    token: thisIsMyToken
    name: TestFilterGroup
    state: absent
"""

RETURN = r"""
dynamic_group:
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
    NB_DYNAMIC_GROUPS,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            group_type=dict(required=False, type="str", choices=["dynamic-filter", "dynamic-set", "static"]),
            content_type=dict(required=False, type="str"),
            tenant=dict(required=False, type="raw"),
            filter=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    dynamic_group = NautobotExtrasModule(module, NB_DYNAMIC_GROUPS)
    dynamic_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
