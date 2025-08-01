#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: secrets_group
short_description: Creates or removes secrets groups from Nautobot
description:
  - Creates or removes secrets groups from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.11.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the secrets group
      - Required if I(state=present) and the secrets group does not exist yet
    required: false
    type: str
  description:
    description:
      - A description of the secrets group
    required: false
    type: str
"""

EXAMPLES = r"""
---
- name: Create a secrets group
  networktocode.nautobot.secrets_group:
    url: http://nautobot.local
    token: thisIsMyToken
    name: my_secrets_group
    description: My secrets group

- name: Delete a secrets group
  networktocode.nautobot.secrets_group:
    url: http://nautobot.local
    token: thisIsMyToken
    name: my_secrets_group
    state: absent

- name: Delete a secrets group by id
  networktocode.nautobot.secrets_group:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
secrets_group:
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
    NB_SECRETS_GROUP,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    secrets_group = NautobotExtrasModule(module, NB_SECRETS_GROUP)
    secrets_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
