#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: metadata_choice
short_description: Create, update or delete metadata choices within Nautobot
description:
  - Creates, updates or removes metadata choices from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
version_added: "5.5.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  metadata_type:
    description:
      - The name of the metadata type
    required: true
    type: str
  value:
    description:
      - The value of the metadata choice
    required: true
    type: str
  weight:
    description:
      - Weight of this choice
    required: false
    type: int
"""

EXAMPLES = r"""
- name: Create a metadata choice
  networktocode.nautobot.metadata_choice:
    url: http://nautobot.local
    token: thisIsMyToken
    value: "Choice 1"
    weight: 100
    metadata_type: "TopSecretInfo"
    state: present

- name: Delete a metadata choice
  networktocode.nautobot.metadata_choice:
    url: http://nautobot.local
    token: thisIsMyToken
    value: "Choice 1"
    metadata_type: "TopSecretInfo"
    state: absent
"""

RETURN = r"""
metadata_choice:
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
    NB_METADATA_CHOICES,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            metadata_type=dict(required=True, type="str"),
            value=dict(required=True, type="str"),
            weight=dict(required=False, type="int"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    metadata_choice = NautobotExtrasModule(module, NB_METADATA_CHOICES)
    metadata_choice.run()


if __name__ == "__main__":  # pragma: no cover
    main()
