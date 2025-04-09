#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: secrets_groups_association
short_description: Associates secrets to secrets groups
description:
  - Associates secrets to secrets groups
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
options:
  access_type:
    description:
      - The access type of the secret
    required: true
    type: str
    choices:
      - Generic
      - Console
      - gNMI
      - HTTP(S)
      - NETCONF
      - REST
      - RESTCONF
      - SNMP
      - SSH
  secret_type:
    description:
      - The type of the secret
    required: true
    type: str
    choices:
      - key
      - password
      - secret
      - token
      - username
  secrets_group:
    description:
      - The name of the secrets group to associate the secret to
    required: true
    type: str
  secret:
    description:
      - The name of the secret to associate to the secrets group
    required: true
    type: str
"""

EXAMPLES = r"""
---
- name: Associate a secret to a secrets group
  networktocode.nautobot.secrets_groups_association:
    url: http://nautobot.local
    token: thisIsMyToken
    access_type: Generic
    secret_type: key
    secrets_group: My Secrets Group
    secret: My Secret

- name: Remove a secret from a secrets group
  networktocode.nautobot.secrets_groups_association:
    url: http://nautobot.local
    token: thisIsMyToken
    access_type: Generic
    secret_type: key
    secrets_group: My Secrets Group
    secret: My Secret
    state: absent
"""

RETURN = r"""
secrets_groups_association:
  description: The secrets groups association
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_SECRETS_GROUPS_ASSOCIATION,
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
            access_type=dict(required=True, type="str", choices=["Generic", "Console", "gNMI", "HTTP(S)", "NETCONF", "REST", "RESTCONF", "SNMP", "SSH"]),
            secret_type=dict(required=True, type="str", choices=["key", "password", "secret", "token", "username"]),
            secrets_group=dict(required=True, type="str", no_log=False),
            secret=dict(required=True, type="str", no_log=False),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    secrets_groups_association = NautobotExtrasModule(module, NB_SECRETS_GROUPS_ASSOCIATION)
    secrets_groups_association.run()


if __name__ == "__main__":
    main()
