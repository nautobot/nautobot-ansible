#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_family
short_description: Create, update or delete device families within Nautobot
description:
  - Creates, updates or removes device families from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.16.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the device family
    required: false
    type: str
  description:
    description:
      - The description of the device family
    required: false
    type: str
"""

EXAMPLES = r"""
- name: Create a device family
  networktocode.nautobot.device_family:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Device Family"
    description: "This is a device family"
    state: present

- name: Delete a device family
  networktocode.nautobot.device_family:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Device Family"
    state: absent

- name: Delete a device family by id
  networktocode.nautobot.device_family:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
device_family:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating successful operation
  returned: success
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_DEVICE_FAMILIES,
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
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    device_family = NautobotDcimModule(module, NB_DEVICE_FAMILIES)
    device_family.run()


if __name__ == "__main__":  # pragma: no cover
    main()
