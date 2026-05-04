#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: provider_network
short_description: Create, update or delete provider networks within Nautobot
description:
  - Creates, updates or removes provider networks from Nautobot
deprecated:
  removed_in: "7.0.0"
  why: Provider networks are managed on the I(provider) record.
  alternative: Use M(networktocode.nautobot.provider) with I(provider_networks).
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Josh VanDeraa (@jvanderaa)
requirements:
  - pynautobot
version_added: "6.2.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the provider network
      - Required if I(state=present) and the provider network does not exist yet
    required: false
    type: str
  circuit_provider:
    description:
      - The provider that this network belongs to
      - Required if I(state=present) and the provider network does not exist yet
    required: false
    type: raw
    aliases:
      - provider
  description:
    description:
      - A description of the provider network
    required: false
    type: str
  comments:
    description:
      - Comments related to the provider network
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create provider network within Nautobot with only required information
      networktocode.nautobot.provider_network:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider Network
        provider: Test Provider
        state: present

    - name: Update provider network with other fields
      networktocode.nautobot.provider_network:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider Network
        provider: Test Provider
        description: "A test provider network"
        comments: "Some comments"
        state: present

    - name: Delete provider network within nautobot
      networktocode.nautobot.provider_network:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider Network
        provider: Test Provider
        state: absent

    - name: Delete provider network by id
      networktocode.nautobot.provider_network:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
provider_network:
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
    NB_PROVIDER_NETWORKS,
    NautobotCircuitsModule,
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
            circuit_provider=dict(required=False, type="raw", aliases=["provider"]),
            description=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
        ),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    provider_network = NautobotCircuitsModule(module, NB_PROVIDER_NETWORKS)
    provider_network.run()


if __name__ == "__main__":  # pragma: no cover
    main()
