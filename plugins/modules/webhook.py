#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: webhook
short_description: Creates or removes webhooks from Nautobot
description:
  - Creates or removes webhooks from Nautobot
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
  content_types:
    required: true
    type: list
  name:
    required: true
    type: str
  type_create:
    required: false
    type: bool
  type_update:
    required: false
    type: bool
  type_delete:
    required: false
    type: bool
  payload_url:
    required: true
    type: str
  enabled:
    required: false
    type: bool
  http_method:
    required: false
    type: str
    choices:
      - "GET"
      - "POST"
      - "PUT"
      - "PATCH"
      - "DELETE"
  http_content_type:
    required: false
    type: str
  additional_headers:
    required: false
    type: str
  body_template:
    required: false
    type: str
  secret:
    required: false
    type: str
  ssl_verification:
    required: false
    type: bool
  ca_file_path:
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create webhook within Nautobot with only required information
      networktocode.nautobot.webhook:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Webhook
        content_types: None
        payload_url: "Test payload_url"
        state: present

    - name: Delete webhook within nautobot
      networktocode.nautobot.webhook:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Webhook
        state: absent
"""

RETURN = r"""
webhook:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_WEBHOOKS,
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
            content_types=dict(required=True, type="list"),
            name=dict(required=True, type="str"),
            type_create=dict(required=False, type="bool"),
            type_update=dict(required=False, type="bool"),
            type_delete=dict(required=False, type="bool"),
            payload_url=dict(required=True, type="str"),
            enabled=dict(required=False, type="bool"),
            http_method=dict(
                required=False,
                type="str",
                choices=[
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                ],
            ),
            http_content_type=dict(required=False, type="str"),
            additional_headers=dict(required=False, type="str"),
            body_template=dict(required=False, type="str"),
            secret=dict(required=False, type="str"),
            ssl_verification=dict(required=False, type="bool"),
            ca_file_path=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    webhook = NautobotExtrasModule(module, NB_WEBHOOKS)
    webhook.run()


if __name__ == "__main__":  # pragma: no cover
    main()
