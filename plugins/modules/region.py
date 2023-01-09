#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: region
short_description: Creates or removes regions from Nautobot
description:
  - Creates or removes regions from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  name:
    description:
      - Name of the region to be created
    required: true
    type: str
    version_added: "3.0.0"
  slug:
    description:
      - The slugified version of the name or custom slug.
      - This is auto-generated following Nautobot rules if not provided
    required: false
    type: str
    version_added: "3.0.0"
  parent_region:
    description:
      - The parent region this region should be tied to
    required: false
    type: raw
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot region module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create tenant within Nautobot with only required information
      networktocode.nautobot.region:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "Test Region One"
        state: present

    - name: Delete tenant within nautobot
      networktocode.nautobot.region:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant Group ABC
        state: absent
"""

RETURN = r"""
region:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_REGIONS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            slug=dict(required=False, type="str"),
            parent_region=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    region = NautobotDcimModule(module, NB_REGIONS)
    region.run()


if __name__ == "__main__":  # pragma: no cover
    main()
