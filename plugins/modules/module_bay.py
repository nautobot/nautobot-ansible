#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: module_bay
short_description: Create, update or delete module bays within Nautobot
description:
  - Creates, updates or removes module bays from Nautobot
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
  parent_device:
    description:
      - The parent device of the module bay
      - Requires one of I(parent_device) or I(parent_module) when I(state=present) and the module bay does not exist yet
    required: false
    type: raw
  parent_module:
    description:
      - The parent module of the module bay
      - Requires one of I(parent_device) or I(parent_module) when I(state=present) and the module bay does not exist yet
    required: false
    type: raw
  name:
    description:
      - The name of the module bay
      - Required if I(state=present) and the module bay does not exist yet
    required: false
    type: str
  label:
    description:
      - The label of the module bay
    required: false
    type: str
  position:
    description:
      - The position of the module bay within the device or module
    required: false
    type: str
  description:
    description:
      - The description of the module bay
    required: false
    type: str
"""

EXAMPLES = r"""
- name: Create a module bay inside a device
  networktocode.nautobot.module_bay:
    url: http://nautobot.local
    token: thisIsMyToken
    parent_device: test100
    name: Watch Bay
    label: watchbay
    position: "42"
    description: The bay of watches
    state: present

- name: Create a module bay inside a module
  networktocode.nautobot.module_bay:
    url: http://nautobot.local
    token: thisIsMyToken
    parent_module:
      module_type: HooverMaxProModel60
      parent_module_bay: "{{ some_module_bay['key'] }}"
    name: Fixing Good
    label: FiXiNgGoOd
    position: "321"
    description: Good Fixing is better than Bad Breaking
    state: present

- name: Delete a module bay
  networktocode.nautobot.module_bay:
    url: http://nautobot.local
    token: thisIsMyToken
    parent_device: test100
    name: Watch Bay
    state: absent

- name: Delete a module bay by id
  networktocode.nautobot.module_bay:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
module_bay:
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
    NB_MODULE_BAYS,
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
            parent_device=dict(required=False, type="raw"),
            parent_module=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            label=dict(required=False, type="str"),
            position=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    module_bay = NautobotDcimModule(module, NB_MODULE_BAYS)
    module_bay.run()


if __name__ == "__main__":  # pragma: no cover
    main()
