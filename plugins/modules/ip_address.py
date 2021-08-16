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
module: ip_address
short_description: Creates or removes IP addresses from Nautobot
description:
  - Creates or removes IP addresses from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
  - Anthony Ruhier (@Anthony25)
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
  address:
    description:
      - Required if state is C(present)
    required: false
    type: str
  prefix:
    description:
      - |
        With state C(present), if an interface is given, it will ensure
        that an IP inside this prefix (and vrf, if given) is attached
        to this interface. Otherwise, it will get the next available IP
        of this prefix and attach it.
        With state C(new), it will force to get the next available IP in
        this prefix. If an interface is given, it will also force to attach
        it.
        Required if state is C(present) or C(new) when no address is given.
        Unused if an address is specified.
    required: false
    type: raw
  vrf:
    description:
      - VRF that IP address is associated with
    required: false
    type: raw
  tenant:
    description:
      - The tenant that the device will be assigned to
    required: false
    type: raw
  status:
    description:
      - The status of the IP address
    required: false
    type: raw
  role:
    description:
      - The role of the IP address
    choices:
      - Loopback
      - Secondary
      - Anycast
      - VIP
      - VRRP
      - HSRP
      - GLBP
      - CARP
    required: false
    type: str
  description:
    description:
      - The description of the interface
    required: false
    type: str
  nat_inside:
    description:
      - The inside IP address this IP is assigned to
    required: false
    type: raw
  dns_name:
    description:
      - Hostname or FQDN
    required: false
    type: str
  assigned_object:
    description:
      - Definition of the assigned object.
    required: false
    type: dict
    suboptions:
      name:
        description:
          - The name of the interface
        type: str
        required: False
      device:
        description:
          - The device the interface is attached to.
        type: str
        required: False
      virtual_machine:
        description:
          - The virtual machine the interface is attached to.
        type: str
        required: False
  tags:
    description:
      - Any tags that the IP address may need to be associated with
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
      - |
        Use C(present), C(new) or C(absent) for adding, force adding or removing.
        C(present) will check if the IP is already created, and return it if
        true. C(new) will force to create it anyway (useful for anycasts, for
        example).
    choices: [ absent, new, present ]
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
- name: "Test Nautobot IP address module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create IP address within Nautobot with only required information
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        status: active
        state: present
    - name: Force to create (even if it already exists) the IP
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        state: new
    - name: Get a new available IP inside 192.168.1.0/24
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 192.168.1.0/24
        state: new
    - name: Delete IP address within nautobot
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        state: absent
    - name: Create IP address with several specified options
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        family: 4
        address: 192.168.1.20
        vrf: Test
        tenant: Test Tenant
        status: Reserved
        role: Loopback
        description: Test description
        tags:
          - Schnozzberry
        state: present
    - name: Create IP address and assign a nat_inside IP
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        family: 4
        address: 192.168.1.30
        vrf: Test
        nat_inside:
          address: 192.168.1.20
          vrf: Test
        assigned_object:
          name: GigabitEthernet1
          device: test100
    - name: Ensure that an IP inside 192.168.1.0/24 is attached to GigabitEthernet1
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 192.168.1.0/24
        vrf: Test
        assigned_object:
          name: GigabitEthernet1
          device: test100
        state: present
    - name: Attach a new available IP of 192.168.1.0/24 to GigabitEthernet1
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 192.168.1.0/24
        vrf: Test
        assigned_object:
          name: GigabitEthernet1
          device: test100
        state: new
"""

RETURN = r"""
ip_address:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_IP_ADDRESSES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    # state choices present, absent, new
    argument_spec["state"] = dict(
        required=False, default="present", choices=["present", "absent", "new"]
    )
    argument_spec.update(
        dict(
            address=dict(required=False, type="str"),
            prefix=dict(required=False, type="raw"),
            vrf=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            role=dict(
                required=False,
                type="str",
                choices=[
                    "Loopback",
                    "Secondary",
                    "Anycast",
                    "VIP",
                    "VRRP",
                    "HSRP",
                    "GLBP",
                    "CARP",
                ],
            ),
            description=dict(required=False, type="str"),
            nat_inside=dict(required=False, type="raw"),
            dns_name=dict(required=False, type="str"),
            assigned_object=dict(
                required=False,
                type="dict",
                options=dict(
                    name=dict(required=False, type="str"),
                    device=dict(required=False, type="str"),
                    virtual_machine=dict(required=False, type="str"),
                ),
            ),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    required_if = [
        ("state", "present", ["address", "prefix", "status"], True),
        ("state", "absent", ["address"]),
        ("state", "new", ["address", "prefix"], True),
    ]
    mutually_exclusive = [["address", "prefix"]]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
    )

    ip_address = NautobotIpamModule(module, NB_IP_ADDRESSES)
    ip_address.run()


if __name__ == "__main__":  # pragma: no cover
    main()
