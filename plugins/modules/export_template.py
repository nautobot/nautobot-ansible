#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: export_template
short_description: Creates or removes export templates from Nautobot
description:
  - Creates or removes export templates from Nautobot
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
  owner_content_type:
    required: false
    type: str
  owner_object_id:
    required: false
    type: str
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  template_code:
    required: true
    type: str
  mime_type:
    required: false
    type: str
  file_extension:
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create export template within Nautobot with only required information
      networktocode.nautobot.export_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Export Template
        content_type: "Test content_type"
        template_code: "Test template_code"
        state: present

    - name: Delete export_template within nautobot
      networktocode.nautobot.export_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Export_Template
        state: absent
"""

RETURN = r"""
export_template:
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
    NB_EXPORT_TEMPLATES,
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
            owner_content_type=dict(required=False, type="str"),
            owner_object_id=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            template_code=dict(required=True, type="str"),
            mime_type=dict(required=False, type="str"),
            file_extension=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    export_template = NautobotExtrasModule(module, NB_EXPORT_TEMPLATES)
    export_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
