#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: provider
short_description: Creates or removes providers from Nautobot
description:
  - Creates or removes providers from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  asn:
    required: false
    type: int
  account:
    required: false
    type: str
  portal_url:
    required: false
    type: str
  noc_contact:
    required: false
    type: str
  admin_contact:
    required: false
    type: str
  comments:
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create provider within Nautobot with only required information
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        state: present

    - name: Delete provider within nautobot
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        state: absent
"""

RETURN = r"""
provider:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.circuits import (
    NB_PROVIDERS,
    NautobotCircuitsModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            asn=dict(required=False, type="int"),
            account=dict(required=False, type="str"),
            portal_url=dict(required=False, type="str"),
            noc_contact=dict(required=False, type="str"),
            admin_contact=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    provider = NautobotCircuitsModule(module, NB_PROVIDERS)
    provider.run()


if __name__ == "__main__":  # pragma: no cover
    main()
