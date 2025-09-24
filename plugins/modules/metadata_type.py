#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: metadata_type
short_description: Create, update or delete metadata types within Nautobot
description:
  - Creates, updates or removes metadata types from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
version_added: "5.5.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the metadata type
      - Required if I(state=present) and the metadata type does not exist yet
    required: false
    type: str
  description:
    description:
      - The description of the metdata type
    required: false
    type: str
  data_type:
    description:
      - Data type of this field
      - Required if I(state=present) and the metadata type does not exist yet
    required: false
    choices:
      - text
      - integer
      - boolean
      - date
      - url
      - select
      - multi-select
      - json
      - markdown
      - contact-or-team
      - datetime
      - float
    type: str
  content_types:
    description:
      - Content types that this metadata type should be available for
      - Required if I(state=present) and the metadata type does not exist yet
    required: false
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: Create a metadata type
  networktocode.nautobot.metadata_type:
    url: http://nautobot.local
    token: thisIsMyToken
    name: TopSecretInfo
    description: The topest secretest info
    data_type: text
    content_types:
      - dcim.device
    state: present

- name: Delete a metadata type
  networktocode.nautobot.metadata_type:
    url: http://nautobot.local
    token: thisIsMyToken
    name: TopSecretInfo
    state: absent

- name: Delete a metadata type by id
  networktocode.nautobot.metadata_type:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
metadata_type:
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
    NB_METADATA_TYPES,
    NautobotExtrasModule,
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
            description=dict(required=False, type="str"),
            data_type=dict(
                required=False,
                choices=[
                    "text",
                    "integer",
                    "boolean",
                    "date",
                    "url",
                    "select",
                    "multi-select",
                    "json",
                    "markdown",
                    "contact-or-team",
                    "datetime",
                    "float",
                ],
                type="str",
            ),
            content_types=dict(required=False, type="list", elements="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    metadata_type = NautobotExtrasModule(module, NB_METADATA_TYPES)
    metadata_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
