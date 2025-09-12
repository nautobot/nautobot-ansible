#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: graphql_query
short_description: Creates or removes graphql queries from Nautobot
description:
  - Creates or removes graphql queries from Nautobot
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
  owner_content_type:
    required: false
    type: str
  owner_object_id:
    required: false
    type: str
  name:
    required: true
    type: str
  query:
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create graphql query within Nautobot with only required information
      networktocode.nautobot.graphql_query:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Graphql Query
        query: "Test query"
        state: present

    - name: Delete graphql_query within nautobot
      networktocode.nautobot.graphql_query:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Graphql_Query
        state: absent
"""

RETURN = r"""
graphql_query:
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
    NB_GRAPHQL_QUERIES,
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
            owner_content_type=dict(required=False, type="str"),
            owner_object_id=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            query=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    graphql_query = NautobotExtrasModule(module, NB_GRAPHQL_QUERIES)
    graphql_query.run()


if __name__ == "__main__":  # pragma: no cover
    main()
