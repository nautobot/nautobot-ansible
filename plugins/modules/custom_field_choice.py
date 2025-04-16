#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: custom_field_choice
short_description: Creates or removes custom field choices from Nautobot
description:
  - Creates or removes custom field choices from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.1.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  value:
    description:
      - Value of this choice
    required: true
    type: str
    version_added: "5.1.0"
  weight:
    description:
      - Weight of this choice
    required: false
    type: int
    version_added: "5.1.0"
  custom_field:
    description:
      - Custom field this choice belongs to
    required: true
    type: raw
    version_added: "5.1.0"
"""

EXAMPLES = r"""
---
- name: Create a custom field choice
  networktocode.nautobot.custom_field_choice:
    url: http://nautobot.local
    token: thisIsMyToken
    value: "Choice 1"
    weight: 100
    custom_field: "Custom Field 1"
    state: present
"""

RETURN = r"""
custom_field_choice:
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
    NB_CUSTOM_FIELD_CHOICES,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """Execute custom field choice module."""
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            value=dict(required=True, type="str"),
            weight=dict(required=False, type="int"),
            custom_field=dict(required=True, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    custom_field_choice = NautobotExtrasModule(module, NB_CUSTOM_FIELD_CHOICES)
    custom_field_choice.run()


if __name__ == "__main__":  # pragma: no cover
    main()
