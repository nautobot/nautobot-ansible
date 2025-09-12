#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: git_repository
short_description: Creates or removes git repositories from Nautobot
description:
  - Creates or removes git repositories from Nautobot
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
  provided_contents:
    required: false
    type: list
  name:
    required: true
    type: str
  slug:
    required: false
    type: str
  remote_url:
    required: true
    type: str
  branch:
    required: false
    type: str
  current_head:
    required: false
    type: str
  secrets_group:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create git_repository within Nautobot with only required information
      networktocode.nautobot.git_repository:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Git_Repository
        remote_url: "Test remote_url"
        state: present

    - name: Delete git_repository within nautobot
      networktocode.nautobot.git_repository:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Git_Repository
        state: absent
"""

RETURN = r"""
git_repository:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_GIT_REPOSITORIES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            provided_contents=dict(required=False, type="list"),
            name=dict(required=True, type="str"),
            slug=dict(required=False, type="str"),
            remote_url=dict(required=True, type="str"),
            branch=dict(required=False, type="str"),
            current_head=dict(required=False, type="str"),
            secrets_group=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    git_repository = NautobotExtrasModule(module, NB_GIT_REPOSITORIES)
    git_repository.run()


if __name__ == "__main__":  # pragma: no cover
    main()
