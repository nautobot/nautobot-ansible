#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: namespace
short_description: Creates or removes namespaces from Nautobot
description:
  - Creates or removes namespaces from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.1.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the namespace
    required: true
    type: str
    version_added: "5.1.0"
  description:
    description:
      - The description of the namespace
    required: false
    type: str
    version_added: "5.1.0"
  location:
    description:
      - The location of the namespace
    required: false
    type: raw
    version_added: "5.1.0"
"""

EXAMPLES = r"""
---
- name: Create a namespace
  networktocode.nautobot.namespace:
    url: http://nautobot.local
    token: thisIsMyToken
    name: My Namespace
    location: My Location
    description: My Description
    tags:
      - tag1
      - tag2
    custom_fields:
      my_custom_field: my_value
    state: present

- name: Delete a namespace
  networktocode.nautobot.namespace:
    url: http://nautobot.local
    token: thisIsMyToken
    name: My Namespace
    state: absent
"""

RETURN = r"""
namespace:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_NAMESPACES,
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
            description=dict(required=False, type="str"),
            location=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    namespace = NautobotDcimModule(module, NB_NAMESPACES)
    namespace.run()


if __name__ == "__main__":  # pragma: no cover
    main()
