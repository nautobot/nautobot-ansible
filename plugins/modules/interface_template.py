#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: interface_template
short_description: Creates or removes interface templates from Nautobot
description:
  - Creates or removes interface templates from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  label:
    required: false
    type: str
  description:
    required: false
    type: str
  type:
    required: true
    type: str
    choices:
      - "1000base-kx"
      - "1000base-t"
      - "1000base-x-gbic"
      - "1000base-x-sfp"
      - "100base-fx"
      - "100base-lfx"
      - "100base-t1"
      - "100base-tx"
      - "100gbase-kp4"
      - "100gbase-kr2"
      - "100gbase-kr4"
      - "100gbase-x-cfp"
      - "100gbase-x-cfp2"
      - "100gbase-x-cfp4"
      - "100gbase-x-cpak"
      - "100gbase-x-cxp"
      - "100gbase-x-dsfp"
      - "100gbase-x-qsfp28"
      - "100gbase-x-qsfpdd"
      - "100gbase-x-sfpdd"
      - "10g-epon"
      - "10gbase-cx4"
      - "10gbase-kr"
      - "10gbase-kx4"
      - "10gbase-t"
      - "10gbase-x-sfpp"
      - "10gbase-x-x2"
      - "10gbase-x-xenpak"
      - "10gbase-x-xfp"
      - "128gfc-sfp28"
      - "1600gbase-x-osfp"
      - "1600gbase-x-osfp-xd"
      - "16gfc-sfpp"
      - "1gfc-sfp"
      - "2.5gbase-t"
      - "200gbase-x-cfp2"
      - "200gbase-x-qsfp56"
      - "200gbase-x-qsfpdd"
      - "25gbase-kr"
      - "25gbase-x-sfp28"
      - "2gfc-sfp"
      - "32gfc-sfp28"
      - "32gfc-sfpp"
      - "400gbase-x-cdfp"
      - "400gbase-x-cfp2"
      - "400gbase-x-cfp8"
      - "400gbase-x-osfp"
      - "400gbase-x-osfp-rhs"
      - "400gbase-x-qsfp112"
      - "400gbase-x-qsfpdd"
      - "40gbase-kr4"
      - "40gbase-x-qsfpp"
      - "4gfc-sfp"
      - "50gbase-kr"
      - "50gbase-x-sfp28"
      - "50gbase-x-sfp56"
      - "5gbase-t"
      - "64gfc-qsfpp"
      - "64gfc-sfpdd"
      - "64gfc-sfpp"
      - "800gbase-x-osfp"
      - "800gbase-x-osfp-xd"
      - "800gbase-x-qsfpdd"
      - "8gfc-sfpp"
      - "bridge"
      - "cdma"
      - "cisco-flexstack"
      - "cisco-flexstack-plus"
      - "cisco-stackwise"
      - "cisco-stackwise-160"
      - "cisco-stackwise-1t"
      - "cisco-stackwise-320"
      - "cisco-stackwise-480"
      - "cisco-stackwise-80"
      - "cisco-stackwise-plus"
      - "da15"
      - "da26"
      - "da31"
      - "db25"
      - "db44"
      - "db60"
      - "dc37"
      - "dc62"
      - "dc79"
      - "dd100"
      - "dd50"
      - "dd78"
      - "de15"
      - "de19"
      - "de9"
      - "df104"
      - "docsis"
      - "e1"
      - "e3"
      - "epon"
      - "extreme-summitstack"
      - "extreme-summitstack-128"
      - "extreme-summitstack-256"
      - "extreme-summitstack-512"
      - "gpon"
      - "gsm"
      - "ieee802.11a"
      - "ieee802.11ac"
      - "ieee802.11ad"
      - "ieee802.11ax"
      - "ieee802.11ay"
      - "ieee802.11g"
      - "ieee802.11n"
      - "ieee802.15.1"
      - "infiniband-ddr"
      - "infiniband-edr"
      - "infiniband-fdr"
      - "infiniband-fdr10"
      - "infiniband-hdr"
      - "infiniband-ndr"
      - "infiniband-qdr"
      - "infiniband-sdr"
      - "infiniband-xdr"
      - "juniper-vcp"
      - "lag"
      - "lte"
      - "ng-pon2"
      - "other"
      - "other-wireless"
      - "sonet-oc12"
      - "sonet-oc192"
      - "sonet-oc1920"
      - "sonet-oc3"
      - "sonet-oc3840"
      - "sonet-oc48"
      - "sonet-oc768"
      - "t1"
      - "t3"
      - "virtual"
      - "xdsl"
      - "xg-pon"
      - "xgs-pon"
  mgmt_only:
    required: false
    type: bool
  device_type:
    required: false
    type: dict
  module_type:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create interface template within Nautobot with only required information
      networktocode.nautobot.interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface Template
        type: 1000base-kx
        state: present

    - name: Delete interface_template within nautobot
      networktocode.nautobot.interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface Template
        state: absent
"""

RETURN = r"""
interface_template:
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
    NB_INTERFACE_TEMPLATES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            type=dict(
                required=True,
                type="str",
                choices=[
                    "1000base-kx",
                    "1000base-t",
                    "1000base-x-gbic",
                    "1000base-x-sfp",
                    "100base-fx",
                    "100base-lfx",
                    "100base-t1",
                    "100base-tx",
                    "100gbase-kp4",
                    "100gbase-kr2",
                    "100gbase-kr4",
                    "100gbase-x-cfp",
                    "100gbase-x-cfp2",
                    "100gbase-x-cfp4",
                    "100gbase-x-cpak",
                    "100gbase-x-cxp",
                    "100gbase-x-dsfp",
                    "100gbase-x-qsfp28",
                    "100gbase-x-qsfpdd",
                    "100gbase-x-sfpdd",
                    "10g-epon",
                    "10gbase-cx4",
                    "10gbase-kr",
                    "10gbase-kx4",
                    "10gbase-t",
                    "10gbase-x-sfpp",
                    "10gbase-x-x2",
                    "10gbase-x-xenpak",
                    "10gbase-x-xfp",
                    "128gfc-sfp28",
                    "1600gbase-x-osfp",
                    "1600gbase-x-osfp-xd",
                    "16gfc-sfpp",
                    "1gfc-sfp",
                    "2.5gbase-t",
                    "200gbase-x-cfp2",
                    "200gbase-x-qsfp56",
                    "200gbase-x-qsfpdd",
                    "25gbase-kr",
                    "25gbase-x-sfp28",
                    "2gfc-sfp",
                    "32gfc-sfp28",
                    "32gfc-sfpp",
                    "400gbase-x-cdfp",
                    "400gbase-x-cfp2",
                    "400gbase-x-cfp8",
                    "400gbase-x-osfp",
                    "400gbase-x-osfp-rhs",
                    "400gbase-x-qsfp112",
                    "400gbase-x-qsfpdd",
                    "40gbase-kr4",
                    "40gbase-x-qsfpp",
                    "4gfc-sfp",
                    "50gbase-kr",
                    "50gbase-x-sfp28",
                    "50gbase-x-sfp56",
                    "5gbase-t",
                    "64gfc-qsfpp",
                    "64gfc-sfpdd",
                    "64gfc-sfpp",
                    "800gbase-x-osfp",
                    "800gbase-x-osfp-xd",
                    "800gbase-x-qsfpdd",
                    "8gfc-sfpp",
                    "bridge",
                    "cdma",
                    "cisco-flexstack",
                    "cisco-flexstack-plus",
                    "cisco-stackwise",
                    "cisco-stackwise-160",
                    "cisco-stackwise-1t",
                    "cisco-stackwise-320",
                    "cisco-stackwise-480",
                    "cisco-stackwise-80",
                    "cisco-stackwise-plus",
                    "da15",
                    "da26",
                    "da31",
                    "db25",
                    "db44",
                    "db60",
                    "dc37",
                    "dc62",
                    "dc79",
                    "dd100",
                    "dd50",
                    "dd78",
                    "de15",
                    "de19",
                    "de9",
                    "df104",
                    "docsis",
                    "e1",
                    "e3",
                    "epon",
                    "extreme-summitstack",
                    "extreme-summitstack-128",
                    "extreme-summitstack-256",
                    "extreme-summitstack-512",
                    "gpon",
                    "gsm",
                    "ieee802.11a",
                    "ieee802.11ac",
                    "ieee802.11ad",
                    "ieee802.11ax",
                    "ieee802.11ay",
                    "ieee802.11g",
                    "ieee802.11n",
                    "ieee802.15.1",
                    "infiniband-ddr",
                    "infiniband-edr",
                    "infiniband-fdr",
                    "infiniband-fdr10",
                    "infiniband-hdr",
                    "infiniband-ndr",
                    "infiniband-qdr",
                    "infiniband-sdr",
                    "infiniband-xdr",
                    "juniper-vcp",
                    "lag",
                    "lte",
                    "ng-pon2",
                    "other",
                    "other-wireless",
                    "sonet-oc12",
                    "sonet-oc192",
                    "sonet-oc1920",
                    "sonet-oc3",
                    "sonet-oc3840",
                    "sonet-oc48",
                    "sonet-oc768",
                    "t1",
                    "t3",
                    "virtual",
                    "xdsl",
                    "xg-pon",
                    "xgs-pon",
                ],
            ),
            mgmt_only=dict(required=False, type="bool"),
            device_type=dict(required=False, type="dict"),
            module_type=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    interface_template = NautobotDcimModule(module, NB_INTERFACE_TEMPLATES)
    interface_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
