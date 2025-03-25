#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_redundancy_group
short_description: Creates or removes device redundancy groups from Nautobot
description:
  - Creates or removes device redundancy groups from Nautobot
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
      - The name of the device redundancy group
    required: true
    type: str
    version_added: "5.1.0"
  status:
    description:
      - The status of the device redundancy group
      - Required if I(state=present) and the device redundancy group does not exist yet
    required: false
    type: raw
    version_added: "5.1.0"
  description:
    description:
      - The description of the device redundancy group
    required: false
    type: str
    version_added: "5.1.0"
  failover_strategy:
    description:
      - The failover strategy of the device redundancy group
    required: false
    choices:
      - active-active
      - active-passive
    type: str
    version_added: "5.1.0"
  secrets_group:
    description:
      - The secrets group of the device redundancy group
    required: false
    type: raw
    version_added: "5.1.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot device_redundancy_group module"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create device redundancy group within Nautobot with only required information
      networktocode.nautobot.device_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Redundancy Group
        status: Active
        state: present
    
    - name: Create device redundancy group within Nautobot with all information
      networktocode.nautobot.device_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Redundancy Group
        status: Active
        description: My Description
        failover_strategy: active-active
        secrets_group: "{{ my_secrets_group['key'] }}"
        tags:
          - My Tag
        custom_fields:
          my_field: my_value
        state: present
      vars:
        my_secrets_group: "{{ lookup('networktocode.nautobot.lookup', 'secrets-groups', api_endpoint=nautobot_url, token=nautobot_token, api_filter='name=\"My Secrets Group\"') }}"
    
    - name: Delete device redundancy group within nautobot
      networktocode.nautobot.device_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Redundancy Group
        state: absent

"""

RETURN = r"""
device_redundancy_group:
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
    NB_DEVICE_REDUNDANCY_GROUPS,
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
            status=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            failover_strategy=dict(
                required=False,
                type="str",
                choices=["active-active", "active-passive"],
            ),
            secrets_group=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    device_redundancy_group = NautobotDcimModule(module, NB_DEVICE_REDUNDANCY_GROUPS)
    device_redundancy_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
