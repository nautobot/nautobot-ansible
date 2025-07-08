#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: module_type
short_description: Create, update or delete module types within Nautobot
description:
  - Creates, updates or removes module types from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
version_added: "5.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  manufacturer:
    description:
      - The manufacturer of the module type
      - Required if I(state=present) and the module type does not exist yet
    required: false
    type: raw
  model:
    description:
      - The model of the module type
    required: true
    type: raw
  part_number:
    description:
      - The part number of the module type
    required: false
    type: str
  comments:
    description:
      - Comments that may include additional information in regards to the module type
    required: false
    type: str
"""

EXAMPLES = r"""
- name: Create a module type
  networktocode.nautobot.module_type:
    url: http://nautobot.local
    token: thisIsMyToken
    model: HooverMaxProModel60
    manufacturer: Best Quality Vacuum
    state: present

- name: Delete a module type
  networktocode.nautobot.module_type:
    url: http://nautobot.local
    token: thisIsMyToken
    model: HooverMaxProModel60
    state: absent
"""

RETURN = r"""
module_type:
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
    NB_MODULE_TYPES,
    NautobotDcimModule,
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
            manufacturer=dict(required=False, type="raw"),
            model=dict(required=True, type="raw"),
            part_number=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    module_type = NautobotDcimModule(module, NB_MODULE_TYPES)
    module_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
