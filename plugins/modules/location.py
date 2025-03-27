#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: location
short_description: Creates or removes locations from Nautobot
description:
  - Creates or removes locations from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "4.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    description:
      - Primary Key of the location, used to delete the location.
      - Because of hierarchical nature of locations and name being not unique across locations,
      - it's a user responsibility to query location and pass its id(PK) to the task to delete the location.
    required: false
    type: str
  name:
    description:
      - Name of the location to be created
    required: false
    type: str
  status:
    description:
      - Status of the location
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
  description:
    description:
      - Location description
    required: false
    type: str
  location_type:
    description:
      - The type of location
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
  parent_location:
    aliases:
      - parent
    description:
      - The parent location this location should be tied to
    required: false
    type: raw
  tenant:
    description:
      - The tenant the location will be assigned to
    required: false
    type: raw
    version_added: "5.1.0"
  facility:
    description:
      - Data center provider or facility, ex. Equinix NY7
    required: false
    type: str
    version_added: "5.1.0"
  asn:
    description:
      - The ASN associated with the location
    required: false
    type: int
    version_added: "5.1.0"
  time_zone:
    description:
      - Timezone associated with the location, ex. America/Denver
    required: false
    type: str
    version_added: "5.1.0"
  physical_address:
    description:
      - Physical address of location
    required: false
    type: str
    version_added: "5.1.0"
  shipping_address:
    description:
      - Shipping address of location
    required: false
    type: str
    version_added: "5.1.0"
  latitude:
    description:
      - Latitude in decimal format
    required: false
    type: str
    version_added: "5.1.0"
  longitude:
    description:
      - Longitude in decimal format
    required: false
    type: str
    version_added: "5.1.0"
  contact_name:
    description:
      - Name of contact for location
    required: false
    type: str
    version_added: "5.1.0"
  contact_phone:
    description:
      - Contact phone number for location
    required: false
    type: str
    version_added: "5.1.0"
  contact_email:
    description:
      - Contact email for location
    required: false
    type: str
    version_added: "5.1.0"
  comments:
    description:
      - Comments for the location. This can be markdown syntax
    required: false
    type: str
    version_added: "5.1.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot location module"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create location
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location
        status: Active
        location_type:
          name: My Location Type
        state: present

    - name: Delete location
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        id: "{{ location_to_delete['key'] }}"
        state: absent
      vars:
        location_to_delete: >-
          {{ lookup(
            'networktocode.nautobot.lookup',
            'locations',
            api_endpoint=nautobot_url,
            token=nautobot_token,
            api_filter='name="My Location" parent_location="Location Parent" location_type="Main Type"'
          ) }}

    - name: Create location with all parameters
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Nested Location
        status: Active
        location_type:
          name: My Location Type
        description: My Nested Location Description
        tenant: Test Tenant
        facility: EquinoxCA7
        asn: "65001"
        time_zone: America/Los Angeles
        physical_address: Hollywood, CA, 90210
        shipping_address: Hollywood, CA, 90210
        latitude: "10.100000"
        longitude: "12.200000"
        contact_name: Jenny
        contact_phone: 867-5309
        contact_email: jenny@example.com
        comments: "**This** is a `markdown` comment"
        parent: My Location
        state: present
"""

RETURN = r"""
location:
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
    TAGS_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_LOCATIONS,
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
            id=dict(required=False, type="str"),
            name=dict(required=False, type="str"),
            status=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            location_type=dict(required=False, type="raw"),
            parent_location=dict(required=False, type="raw", aliases=["parent"]),
            tenant=dict(required=False, type="raw"),
            facility=dict(required=False, type="str"),
            asn=dict(required=False, type="int"),
            time_zone=dict(required=False, type="str"),
            physical_address=dict(required=False, type="str"),
            shipping_address=dict(required=False, type="str"),
            latitude=dict(required=False, type="str"),
            longitude=dict(required=False, type="str"),
            contact_name=dict(required=False, type="str"),
            contact_phone=dict(required=False, type="str"),
            contact_email=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
        )
    )

    required_if = [
        ("state", "absent", ["id"]),
    ]

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    location = NautobotDcimModule(module, NB_LOCATIONS)
    location.run()


if __name__ == "__main__":  # pragma: no cover
    main()
