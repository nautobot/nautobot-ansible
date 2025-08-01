#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: controller_managed_device_group
short_description: Create, update or delete managed device groups within Nautobot
description:
  - Creates, updates or removes managed device groups from Nautobot.
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Sven Winkelmann (@pugnacity)
version_added: "5.7.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the controller managed device groups
      - Required if I(state=present) and the controller managed device group does not exist yet
    required: false
    type: str
  controller:
    description:
      - The name of the controller for this group
      - Required if I(state=present) and the controller managed device group does not exist yet
    required: false
    type: str
  weight:
    description:
      - weight of the managed device group
    required: false
    type: int
  parent_cloud_network:
    aliases:
      - parent
    description:
      - The parent cloud network this network should be child to
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create controller managed device group within Nautobot with only required information
      networktocode.nautobot.controller_managed_device_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "group_1"
        controller: my_controller
        state: present

    - name: Delete controller managed device group within nautobot
      networktocode.nautobot.controller_managed_device_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "group_1"
        controller: test_controller_group_3
        state: absent

    - name: Delete controller managed device group by id
      networktocode.nautobot.controller_managed_device_group:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
controller_managed_device_group:
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
    NB_CONTROLLER_MANAGED_DEVICE_GROUPS,
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
            controller=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
            parent_cloud_network=dict(required=False, type="raw", aliases=["parent"]),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    controller_group = NautobotDcimModule(module, NB_CONTROLLER_MANAGED_DEVICE_GROUPS)
    controller_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
