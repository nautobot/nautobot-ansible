#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
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
module: site
short_description: Creates or removes sites from Nautobot
description:
  - Creates or removes sites from Nautobot
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
      - Name of the site to be created
    required: true
    type: str
  status:
    description:
      - Status of the site
    required: false
    type: raw
  region:
    description:
      - The region that the site should be associated with
    required: false
    type: raw
  tenant:
    description:
      - The tenant the site will be assigned to
    required: false
    type: raw
  facility:
    description:
      - Data center provider or facility, ex. Equinix NY7
    required: false
    type: str
  asn:
    description:
      - The ASN associated with the site
    required: false
    type: int
  time_zone:
    description:
      - Timezone associated with the site, ex. America/Denver
    required: false
    type: str
  description:
    description:
      - The description of the prefix
    required: false
    type: str
  physical_address:
    description:
      - Physical address of site
    required: false
    type: str
  shipping_address:
    description:
      - Shipping address of site
    required: false
    type: str
  latitude:
    description:
      - Latitude in decimal format
    required: false
    type: str
  longitude:
    description:
      - Longitude in decimal format
    required: false
    type: str
  contact_name:
    description:
      - Name of contact for site
    required: false
    type: str
  contact_phone:
    description:
      - Contact phone number for site
    required: false
    type: str
  contact_email:
    description:
      - Contact email for site
    required: false
    type: str
  comments:
    description:
      - Comments for the site. This can be markdown syntax
    required: false
    type: str
  slug:
    description:
      - URL-friendly unique shorthand
    required: false
    type: str
  tags:
    description:
      - Any tags that the prefix may need to be associated with
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
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot site module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create site within Nautobot with only required information
      networktocode.nautobot.site:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test - Colorado
        status: active
        state: present

    - name: Delete site within nautobot
      networktocode.nautobot.site:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test - Colorado
        state: absent

    - name: Create site with all parameters
      networktocode.nautobot.site:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test - California
        status: Planned
        region: Test Region
        tenant: Test Tenant
        facility: EquinoxCA7
        asn: 65001
        time_zone: America/Los Angeles
        description: This is a test description
        physical_address: Hollywood, CA, 90210
        shipping_address: Hollywood, CA, 90210
        latitude: 10.100000
        longitude: 12.200000
        contact_name: Jenny
        contact_phone: 867-5309
        contact_email: jenny@changednumber.com
        slug: test-california
        comments: ### Placeholder
        state: present
"""

RETURN = r"""
site:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_SITES,
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
            status=dict(required=False, type="raw"),
            region=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            facility=dict(required=False, type="str"),
            asn=dict(required=False, type="int"),
            time_zone=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            physical_address=dict(required=False, type="str"),
            shipping_address=dict(required=False, type="str"),
            latitude=dict(required=False, type="str"),
            longitude=dict(required=False, type="str"),
            contact_name=dict(required=False, type="str"),
            contact_phone=dict(required=False, type="str"),
            contact_email=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
            slug=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    required_if = [
        ("state", "present", ["name", "status"]),
        ("state", "absent", ["name"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    site = NautobotDcimModule(module, NB_SITES)
    site.run()


if __name__ == "__main__":  # pragma: no cover
    main()
