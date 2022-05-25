#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: aggregate
short_description: Creates or removes aggregates from Nautobot
description:
  - Creates or removes aggregates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  api_version:
    description:
      - API Version Nautobot REST API
    required: false
    type: str
  url:
    description:
      - "URL of the Nautobot instance resolvable by Ansible control host"
    required: true
    type: str
  token:
    description:
      - "The token created within Nautobot to authorize API access"
    required: true
    type: str
  prefix:
    description:
      - "The aggregate prefix"
    required: true
    type: raw
    version_added: "3.0.0"
  rir:
    description:
      - "The RIR the aggregate will be assigned to"
    required: false
    type: raw
    version_added: "3.0.0"
  date_added:
    description:
      - "Date added, format: YYYY-MM-DD"
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - "The description of the aggregate"
    required: false
    type: str
    version_added: "3.0.0"
  tags:
    description:
      - "Any tags that the aggregate may need to be associated with"
    required: false
    type: list
    elements: raw
    version_added: "3.0.0"
  custom_fields:
    description:
      - "must exist in Nautobot"
    required: false
    type: dict
    version_added: "3.0.0"
  state:
    description:
      - "The state of the aggregate"
    choices: [ present, absent ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
    version_added: "3.0.0"
  validate_certs:
    description:
      - "If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates."
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot aggregate module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create aggregate within Nautobot with only required information
      networktocode.nautobot.aggregate:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 192.168.0.0/16
        rir: Test RIR
        state: present

    - name: Create aggregate with several specified options
      networktocode.nautobot.aggregate:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 192.168.0.0/16
        rir: Test RIR
        date_added: 1989-01-18
        description: Test description
        tags:
          - Schnozzberry
        state: present

    - name: Delete aggregate within nautobot
      networktocode.nautobot.aggregate:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 192.168.0.0/16
        state: absent
"""

RETURN = r"""
aggregate:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_AGGREGATES,
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
            prefix=dict(required=True, type="raw"),
            rir=dict(required=False, type="raw"),
            date_added=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    aggregate = NautobotIpamModule(module, NB_AGGREGATES)
    aggregate.run()


if __name__ == "__main__":  # pragma: no cover
    main()
