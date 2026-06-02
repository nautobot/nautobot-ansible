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
  - networktocode.nautobot.fragments.contacts_and_teams
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
  radio_profiles:
    description:
      - List of radio profiles to associate with this controller managed device group.
    required: false
    type: dict
    version_added: "6.3.0"
    suboptions:
      state:
        description:
          - C(merge) adds associations without removing existing ones.
          - C(replace) enforces exactly the listed associations, removing any extras.
          - C(delete) removes the listed associations.
        required: false
        type: str
        default: merge
        choices: [ merge, replace, delete ]
      objects:
        description:
          - List of radio profiles to associate.
        required: true
        type: list
        elements: dict
        suboptions:
          radio_profile:
            description:
              - The radio profile to associate with the controller managed device group.
            required: true
            type: raw
  wireless_networks:
    description:
      - List of wireless networks to associate with this controller managed device group.
    required: false
    type: dict
    version_added: "6.3.0"
    suboptions:
      state:
        description:
          - C(merge) adds associations without removing existing ones.
          - C(replace) enforces exactly the listed associations, removing any extras.
          - C(delete) removes the listed associations.
        required: false
        type: str
        default: merge
        choices: [ merge, replace, delete ]
      objects:
        description:
          - List of wireless networks to associate.
        required: true
        type: list
        elements: dict
        suboptions:
          wireless_network:
            description:
              - The wireless network to associate with the controller managed device group.
            required: true
            type: raw
          vlan:
            description:
              - Optional VLAN to associate with the wireless network assignment.
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

    - name: Attach radio profiles to a controller managed device group
      networktocode.nautobot.controller_managed_device_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "group_1"
        controller: my_controller
        radio_profiles:
          state: merge
          objects:
            - radio_profile: "Indoor 5GHz"
            - radio_profile: "Outdoor 2.4GHz"
        state: present

    - name: Replace wireless networks on a controller managed device group
      networktocode.nautobot.controller_managed_device_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "group_1"
        controller: my_controller
        wireless_networks:
          state: replace
          objects:
            - wireless_network: "Corp"
              vlan:
                name: "My VLAN"
                vid: 100
            - wireless_network: "Guest"
        state: present
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
    CONTACTS_AND_TEAMS_ARG_SPEC,
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
    argument_spec.update(deepcopy(CONTACTS_AND_TEAMS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            controller=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
            parent_cloud_network=dict(required=False, type="raw", aliases=["parent"]),
            radio_profiles=dict(
                required=False,
                type="dict",
                options=dict(
                    state=dict(required=False, default="merge", choices=["merge", "replace", "delete"]),
                    objects=dict(
                        required=True,
                        type="list",
                        elements="dict",
                        options=dict(
                            radio_profile=dict(required=True, type="raw"),
                        ),
                    ),
                ),
            ),
            wireless_networks=dict(
                required=False,
                type="dict",
                options=dict(
                    state=dict(required=False, default="merge", choices=["merge", "replace", "delete"]),
                    objects=dict(
                        required=True,
                        type="list",
                        elements="dict",
                        options=dict(
                            wireless_network=dict(required=True, type="raw"),
                            vlan=dict(required=False, type="raw"),
                        ),
                    ),
                ),
            ),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    controller_group = NautobotDcimModule(module, NB_CONTROLLER_MANAGED_DEVICE_GROUPS)
    controller_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
