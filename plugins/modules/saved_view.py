#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: saved_view
short_description: Creates or removes saved views from Nautobot
description:
  - Creates or removes saved views from Nautobot
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
  name:
    required: true
    type: str
  view:
    required: true
    type: str
  config:
    required: false
    type: str
  is_global_default:
    required: false
    type: bool
  is_shared:
    required: false
    type: bool
  owner:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create saved_view within Nautobot with only required information
      networktocode.nautobot.saved_view:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Saved_View
        view: "Test view"
        owner: None
        state: present

    - name: Delete saved_view within nautobot
      networktocode.nautobot.saved_view:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Saved_View
        state: absent
"""

RETURN = r"""
saved_view:
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
    NB_SAVED_VIEWS,
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
            name=dict(required=True, type="str"),
            view=dict(required=True, type="str"),
            config=dict(required=False, type="str"),
            is_global_default=dict(required=False, type="bool"),
            is_shared=dict(required=False, type="bool"),
            owner=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    saved_view = NautobotExtrasModule(module, NB_SAVED_VIEWS)
    saved_view.run()


if __name__ == "__main__":  # pragma: no cover
    main()
