#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: custom_link
short_description: Creates or removes custom links from Nautobot
description:
  - Creates or removes custom links from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  id:
    required: false
    type: str
  content_type:
    required: true
    type: str
  name:
    required: true
    type: str
  text:
    required: true
    type: str
  target_url:
    required: true
    type: str
  weight:
    required: false
    type: int
  group_name:
    required: false
    type: str
  button_class:
    required: false
    type: str
  new_window:
    required: true
    type: bool
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create custom_link within Nautobot with only required information
      networktocode.nautobot.custom_link:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Custom_Link
        content_type: "Test content_type"
        text: "Test text"
        target_url: "Test target_url"
        new_window: None
        state: present

    - name: Delete custom_link within nautobot
      networktocode.nautobot.custom_link:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Custom_Link
        state: absent
"""

RETURN = r"""
custom_link:
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
    NB_CUSTOM_LINKS,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            content_type=dict(required=True, type="str"),
            name=dict(required=True, type="str"),
            text=dict(required=True, type="str"),
            target_url=dict(required=True, type="str"),
            weight=dict(required=False, type="int"),
            group_name=dict(required=False, type="str"),
            button_class=dict(required=False, type="str"),
            new_window=dict(required=True, type="bool"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    custom_link = NautobotExtrasModule(module, NB_CUSTOM_LINKS)
    custom_link.run()


if __name__ == "__main__":  # pragma: no cover
    main()
