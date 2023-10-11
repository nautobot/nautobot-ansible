#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: plugin
short_description: CRUD operation on plugin objects
description:
  - Creates, removes or updates various plugin objects in Nautobot
notes:
  - Task must have defined plugin base api url and object endpoint
author:
  - Network to Code (@networktocode)
  - Patryk Szulczewski (@pszulczewski)
version_added: "4.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  plugin:
    description:
      - Plugin API base url
    required: true
    type: str
    version_added: "4.4.0"
  endpoint:
    description:
      - Plugin object API endpoint
    required: true
    type: str
    version_added: "4.4.0"
  identifiers:
    aliases: [ids]
    description:
      - Plugin object identifier(s) like name, model, etc.
    required: true
    type: dict
    version_added: "4.4.0"
  attrs:
    description:
      - Object attributes other than identifier to create or update an object, like description, etc.
    required: false
    type: dict
    version_added: "4.4.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot Plugin Module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create LCM CVE
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: nautobot-device-lifecycle-mgmt
        endpoint: cve
        identifiers:
          name: CVE-2020-7777
        attrs:
          published_date: 2020-09-25
          link: https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory
        state: present

    - name: Modify LCM CVE
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: nautobot-device-lifecycle-mgmt
        endpoint: cve
        identifiers:
          name: CVE-2020-7777
        attrs:
          published_date: 2020-09-25
          link: https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/12345678
        state: present

    - name: Delete LCM CVE
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: nautobot-device-lifecycle-mgmt
        endpoint: cve
        identifiers:
          name: CVE-2020-7777
        state: absent

    - name: Create GC compliance-feature
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: golden-config
        endpoint: compliance-feature
        ids:
          name: AAA
        attrs:
          description: "Authentication Administration Accounting"
        state: present
        
    - name: Create FW address-object
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: firewall
        endpoint: address-object
        ids:
          name: access-point
        attrs:
          ip_address:
            address: 10.0.0.0/32
        state: present

    - name: Delete FW address-object
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: firewall
        endpoint: address-object
        ids:
          name: access-point
        state: absent
"""

RETURN = r"""
endpoint:
  description: Serialized object as created/existent/updated/deleted within Nautobot
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.plugins import (
    NautobotPluginModule,
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
            plugin=dict(required=True, type="str"),
            endpoint=dict(required=True, type="str"),
            identifiers=dict(required=True, type="dict", aliases=["ids"]),
            attrs=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    plugin = NautobotPluginModule(module, "plugins")
    plugin.run()


if __name__ == "__main__":  # pragma: no cover
    main()
