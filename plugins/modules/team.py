#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: team
short_description: Creates or removes teams from Nautobot
description:
  - Creates or removes teams from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the team
    required: true
    type: str
  phone:
    description:
      - The phone number of the team
    required: false
    type: str
  email:
    description:
      - The email of the team
    required: false
    type: str
  address:
    description:
      - The address of the team
    required: false
    type: str
  contacts:
    description:
      - The contacts the team is associated with
    required: false
    type: list
    elements: raw
  comments:
    description:
      - Comments about the team
    required: false
    type: str
"""

EXAMPLES = r"""
---
- name: Create a team
  networktocode.nautobot.team:
    url: http://nautobot.local
    token: thisIsMyToken
    name: My Team
    phone: 123-456-7890
    email: user@example.com
    address: 1234 Main St
    contacts:
      - name: contact1
      - name: contact2
    comments: My Comments
    tags:
      - tag1
      - tag2
    custom_fields:
      my_custom_field: my_value
    state: present

- name: Delete a team
  networktocode.nautobot.team:
    url: http://nautobot.local
    token: thisIsMyToken
    name: My Team
    state: absent
"""

RETURN = r"""
team:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_TEAM,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            phone=dict(required=False, type="str"),
            email=dict(required=False, type="str"),
            address=dict(required=False, type="str"),
            contacts=dict(required=False, type="list", elements="raw"),
            comments=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    team = NautobotExtrasModule(module, NB_TEAM)
    team.run()


if __name__ == "__main__":  # pragma: no cover
    main()
