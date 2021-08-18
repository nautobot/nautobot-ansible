#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: provider
short_description: Create, update or delete providers within Nautobot
description:
  - Creates, updates or removes providers from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  name:
    description:
      - The name of the provider
    required: true
    type: str
  asn:
    description:
      - The provider ASN
    required: false
    type: int
  account:
    description:
      - The account number of the provider
    required: false
    type: str
  portal_url:
    description:
      - The URL of the provider
    required: false
    type: str
  noc_contact:
    description:
      - The NOC contact of the provider
    required: false
    type: str
  admin_contact:
    description:
      - The admin contact of the provider
    required: false
    type: str
  comments:
    description:
      - Comments related to the provider
    required: false
    type: str
  tags:
    description:
      - Any tags that the device may need to be associated with
    required: false
    type: list
    elements: raw
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
    type: dict
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
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
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create provider within Nautobot with only required information
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        state: present

    - name: Update provider with other fields
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        asn: 65001
        account: 200129104
        portal_url: http://provider.net
        noc_contact: noc@provider.net
        admin_contact: admin@provider.net
        comments: "BAD PROVIDER"
        state: present

    - name: Delete provider within nautobot
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        state: absent
"""

RETURN = r"""
provider:
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
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.circuits import (
    NautobotCircuitsModule,
    NB_PROVIDERS,
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
            name=dict(required=True, type="str"),
            asn=dict(required=False, type="int"),
            account=dict(required=False, type="str"),
            portal_url=dict(required=False, type="str"),
            noc_contact=dict(required=False, type="str"),
            admin_contact=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        ),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    provider = NautobotCircuitsModule(module, NB_PROVIDERS)
    provider.run()


if __name__ == "__main__":  # pragma: no cover
    main()
