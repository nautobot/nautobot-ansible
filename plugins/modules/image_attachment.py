#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: image_attachment
short_description: Creates or removes image attachments from Nautobot
description:
  - Creates or removes image attachments from Nautobot
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
  object_id:
    required: true
    type: str
  image:
    required: true
    type: str
  image_height:
    required: true
    type: int
  image_width:
    required: true
    type: int
  name:
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create image_attachment within Nautobot with only required information
      networktocode.nautobot.image_attachment:
        url: http://nautobot.local
        token: thisIsMyToken
        content_type: "Test content_type"
        object_id: "Test object_id"
        image: "Test image"
        image_height: None
        image_width: None
        state: present

    - name: Delete image_attachment within nautobot
      networktocode.nautobot.image_attachment:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
image_attachment:
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
    NB_IMAGE_ATTACHMENTS,
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
            object_id=dict(required=True, type="str"),
            image=dict(required=True, type="str"),
            image_height=dict(required=True, type="int"),
            image_width=dict(required=True, type="int"),
            name=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    image_attachment = NautobotExtrasModule(module, NB_IMAGE_ATTACHMENTS)
    image_attachment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
