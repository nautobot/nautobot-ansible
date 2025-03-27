#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_account
short_description: Creates or removes cloud account from Nautobot
description:
  - Creates or removes cloud account from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
requirements:
  - pynautobot
version_added: "5.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the cloud account
    required: true
    type: str
  account_number:
    description:
      - Required if I(state=present) and the cloud account does not exist yet
    required: false
    type: str
  description:
    description:
      - The description of the cloud account
    required: false
    type: str
  cloud_provider:
    aliases:
      - provider
    description:
      - Required if I(state=present) and the cloud account does not exist yet
    required: false
    type: raw
  secrets_group:
    description:
      - The secrets group of the cloud account
    required: false
    type: raw
"""

EXAMPLES = r"""
---
- name: Create a cloud account
  networktocode.nautobot.cloud_account:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Account
    provider: Cisco
    description: A quantum account for Cisco
    account_number: "654321"
    secrets_group: "{{ my_secrets_group['key'] }}"
    state: present
  vars:
    my_secrets_group: >-
      {{ lookup(
        'networktocode.nautobot.lookup',
        'secrets-groups',
        api_endpoint=nautobot_url,
        token=nautobot_token,
        api_filter='name="My Secrets Group"'
      ) }}

- name: Delete a cloud account
  networktocode.nautobot.cloud_account:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Account
    state: absent
"""

RETURN = r"""
cloud_account:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.cloud import (
    NautobotCloudModule,
    NB_CLOUD_ACCOUNTS,
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
            account_number=dict(required=False, type="str"),
            cloud_provider=dict(required=False, type="raw", aliases=["provider"]),
            secrets_group=dict(required=False, type="raw", no_log=False),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    cloud_account = NautobotCloudModule(module, NB_CLOUD_ACCOUNTS)
    cloud_account.run()


if __name__ == "__main__":  # pragma: no cover
    main()
