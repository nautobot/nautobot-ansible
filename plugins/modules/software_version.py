#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: software_version
short_description: Creates, updates or removes software versions from Nautobot
description:
  - Creates, updates or removes software versions from Nautobot
notes:
  - This module requires Nautobot v2.2+
  - This should be ran with connection C(local) and hosts C(localhost)
  - Tags should be defined as a YAML list
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.7.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  version:
    description:
      - The version of the software
    required: true
    type: str
  platform:
    description:
      - The platform the software will be applied to
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
  status:
    description:
      - The status of the software
      - Required if I(state=present) and does not exist yet
    required: false
    type: str
  alias:
    description:
      - Optional alternative label for this version
    required: false
    type: str
  release_date:
    description:
      - The date the software was released
    required: false
    type: str
  end_of_support_date:
    description:
      - The date the software will no longer be supported
    required: false
    type: str
  documentation_url:
    description:
      - URL to the software documentation
    required: false
    type: str
  long_term_support:
    description:
      - Whether the software is long term support
    required: false
    type: bool
  pre_release:
    description:
      - Whether the software is pre-release
    required: false
    type: bool
"""

EXAMPLES = r"""
---
- name: Create a software version
  networktocode.nautobot.software_version:
    url: http://nautobot.local
    token: thisIsMyToken
    version: 1.0.0
    platform: Cisco IOS
    status: Active
    alias: My Alias
    release_date: 2024-01-01
    end_of_support_date: 2024-12-31
    documentation_url: https://example.com
    long_term_support: true
    pre_release: false
    state: present

- name: Update a software version
  networktocode.nautobot.software_version:
    url: http://nautobot.local
    token: thisIsMyToken
    version: 1.0.0
    state: present

- name: Delete a software version
  networktocode.nautobot.software_version:
    url: http://nautobot.local
    token: thisIsMyToken
    version: 1.0.0
    state: absent
"""

RETURN = r"""
software_version:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_SOFTWARE_VERSIONS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            version=dict(required=True, type="str"),
            platform=dict(required=False, type="raw"),
            status=dict(required=False, type="str"),
            alias=dict(required=False, type="str"),
            release_date=dict(required=False, type="str"),
            end_of_support_date=dict(required=False, type="str"),
            documentation_url=dict(required=False, type="str"),
            long_term_support=dict(required=False, type="bool"),
            pre_release=dict(required=False, type="bool"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    software_version = NautobotDcimModule(module, NB_SOFTWARE_VERSIONS)
    software_version.run()


if __name__ == "__main__":  # pragma: no cover
    main()
