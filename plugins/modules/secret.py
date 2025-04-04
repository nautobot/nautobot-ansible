#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: secret
short_description: Creates or removes secrets from Nautobot
description:
  - Creates or removes secrets from Nautobot
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
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the secret
    required: true
    type: str
  description:
    description:
      - A description of the secret
    required: false
    type: str
  provider:
    description:
      - The provider of the secret (e.g., environment-variable, text-file)
      - Required if I(state=present) and the secret does not exist yet
    required: false
    type: str
  parameters:
    description:
      - A dictionary of parameters for the secret
      - Required if I(state=present) and the secret does not exist yet
    required: false
    type: dict
"""

EXAMPLES = r"""
---
- name: Create an environment variable secret
  networktocode.nautobot.secret:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Device Password
    description: Password for the device
    provider: environment-variable
    parameters:
      variable: NAUTOBOT_NAPALM_PASSWORD
    state: present

- name: Create a text file secret
  networktocode.nautobot.secret:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Device Certificate
    description: Certificate for the device
    provider: text-file
    parameters:
      file: /path/to/device/certificate.pem
    state: present

- name: Delete a secret
  networktocode.nautobot.secret:
    url: http://nautobot.local
    token: thisIsMyToken
    name: My Secret
    state: absent
"""

RETURN = r"""
secret:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_SECRET,
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
            provider=dict(required=False, type="str"),
            parameters=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    secret = NautobotExtrasModule(module, NB_SECRET)
    secret.run()


if __name__ == "__main__":  # pragma: no cover
    main()
