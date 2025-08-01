#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: module_bay_template
short_description: Create, update or delete module bay templates within Nautobot
description:
  - Creates, updates or removes module bay templates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
version_added: "5.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  device_type:
    description:
      - The device type of the module bay template
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the module bay template does not exist yet
    required: false
    type: raw
  module_type:
    description:
      - The module type of the module bay template
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the module bay template does not exist yet
    required: false
    type: raw
  name:
    description:
      - The name of the module bay template
      - Required if I(state=present) and the module bay template does not exist yet
    required: false
    type: str
  label:
    description:
      - The label of the module bay template
    required: false
    type: str
  position:
    description:
      - The position of the module bay within the device or module
    required: false
    type: str
  description:
    description:
      - The description of the module bay template
    required: false
    type: str
"""

EXAMPLES = r"""
- name: Create a module bay template
  networktocode.nautobot.module_bay_template:
    url: http://nautobot.local
    token: thisIsMyToken
    module_type: HooverMaxProModel60
    name: Edward Galbraith
    label: Br Ba
    position: "1"
    description: Granite State
    state: present

- name: Delete a module bay template
  networktocode.nautobot.module_bay_template:
    url: http://nautobot.local
    token: thisIsMyToken
    module_type: HooverMaxProModel60
    name: Edward Galbraith
    state: absent

- name: Delete a module bay template by id
  networktocode.nautobot.module_bay_template:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
module_bay_template:
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
    NB_MODULE_BAY_TEMPLATES,
    NautobotDcimModule,
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
            device_type=dict(required=False, type="raw"),
            module_type=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            label=dict(required=False, type="str"),
            position=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    module_bay_template = NautobotDcimModule(module, NB_MODULE_BAY_TEMPLATES)
    module_bay_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
