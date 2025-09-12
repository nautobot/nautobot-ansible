#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: radio_profile
short_description: Creates or removes radio profiles from Nautobot
description:
  - Creates or removes radio profiles from Nautobot
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
  channel_width:
    required: false
    type: list
  allowed_channel_list:
    required: false
    type: list
  name:
    required: true
    type: str
  frequency:
    required: false
    type: str
    choices:
      - "2.4GHz"
      - "5GHz"
      - "6GHz"
  tx_power_min:
    required: false
    type: int
  tx_power_max:
    required: false
    type: int
  regulatory_domain:
    required: true
    type: str
    choices:
      - "AD"
      - "AE"
      - "AL"
      - "AM"
      - "AU"
      - "AR"
      - "AT"
      - "AZ"
      - "BA"
      - "BE"
      - "BG"
      - "BH"
      - "BN"
      - "BO"
      - "BR"
      - "BS"
      - "BY"
      - "BZ"
      - "CA"
      - "CH"
      - "CI"
      - "CL"
      - "CN"
      - "CO"
      - "CR"
      - "RS"
      - "CY"
      - "CZ"
      - "DE"
      - "DK"
      - "DO"
      - "DZ"
      - "EC"
      - "EE"
      - "EG"
      - "ES"
      - "FO"
      - "FI"
      - "FR"
      - "GB"
      - "GE"
      - "GI"
      - "GL"
      - "GP"
      - "GR"
      - "GT"
      - "GY"
      - "HN"
      - "HK"
      - "HR"
      - "HU"
      - "IS"
      - "IN"
      - "ID"
      - "IE"
      - "IL"
      - "IQ"
      - "IT"
      - "IR"
      - "JM"
      - "JO"
      - "JP"
      - "KP"
      - "KR"
      - "KE"
      - "KW"
      - "KZ"
      - "LB"
      - "LI"
      - "LK"
      - "LT"
      - "LU"
      - "LV"
      - "LY"
      - "MA"
      - "MC"
      - "MD"
      - "MK"
      - "MO"
      - "MQ"
      - "MT"
      - "MU"
      - "MX"
      - "MY"
      - "NA"
      - "NG"
      - "NI"
      - "NL"
      - "NO"
      - "NZ"
      - "OM"
      - "PA"
      - "PE"
      - "PL"
      - "PH"
      - "PK"
      - "PR"
      - "PT"
      - "PY"
      - "QA"
      - "RO"
      - "RU"
      - "SA"
      - "SE"
      - "SG"
      - "SI"
      - "SK"
      - "SM"
      - "SV"
      - "SY"
      - "TH"
      - "TN"
      - "TR"
      - "TT"
      - "TW"
      - "UA"
      - "US"
      - "UY"
      - "UZ"
      - "VA"
      - "VE"
      - "VI"
      - "VN"
      - "YE"
      - "ZA"
      - "ZW"
  rx_power_min:
    required: false
    type: int
  supported_data_rates:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create radio_profile within Nautobot with only required information
      networktocode.nautobot.radio_profile:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Radio_Profile
        regulatory_domain: AD
        state: present

    - name: Delete radio_profile within nautobot
      networktocode.nautobot.radio_profile:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Radio_Profile
        state: absent
"""

RETURN = r"""
radio_profile:
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
    NautobotWirelessModule,
    NB_RADIO_PROFILES,
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
            channel_width=dict(required=False, type="list"),
            allowed_channel_list=dict(required=False, type="list"),
            name=dict(required=True, type="str"),
            frequency=dict(
                required=False,
                type="str",
                choices=[
                    "2.4GHz",
                    "5GHz",
                    "6GHz",
                ],
            ),
            tx_power_min=dict(required=False, type="int"),
            tx_power_max=dict(required=False, type="int"),
            regulatory_domain=dict(
                required=True,
                type="str",
                choices=[
                    "AD",
                    "AE",
                    "AL",
                    "AM",
                    "AU",
                    "AR",
                    "AT",
                    "AZ",
                    "BA",
                    "BE",
                    "BG",
                    "BH",
                    "BN",
                    "BO",
                    "BR",
                    "BS",
                    "BY",
                    "BZ",
                    "CA",
                    "CH",
                    "CI",
                    "CL",
                    "CN",
                    "CO",
                    "CR",
                    "RS",
                    "CY",
                    "CZ",
                    "DE",
                    "DK",
                    "DO",
                    "DZ",
                    "EC",
                    "EE",
                    "EG",
                    "ES",
                    "FO",
                    "FI",
                    "FR",
                    "GB",
                    "GE",
                    "GI",
                    "GL",
                    "GP",
                    "GR",
                    "GT",
                    "GY",
                    "HN",
                    "HK",
                    "HR",
                    "HU",
                    "IS",
                    "IN",
                    "ID",
                    "IE",
                    "IL",
                    "IQ",
                    "IT",
                    "IR",
                    "JM",
                    "JO",
                    "JP",
                    "KP",
                    "KR",
                    "KE",
                    "KW",
                    "KZ",
                    "LB",
                    "LI",
                    "LK",
                    "LT",
                    "LU",
                    "LV",
                    "LY",
                    "MA",
                    "MC",
                    "MD",
                    "MK",
                    "MO",
                    "MQ",
                    "MT",
                    "MU",
                    "MX",
                    "MY",
                    "NA",
                    "NG",
                    "NI",
                    "NL",
                    "NO",
                    "NZ",
                    "OM",
                    "PA",
                    "PE",
                    "PL",
                    "PH",
                    "PK",
                    "PR",
                    "PT",
                    "PY",
                    "QA",
                    "RO",
                    "RU",
                    "SA",
                    "SE",
                    "SG",
                    "SI",
                    "SK",
                    "SM",
                    "SV",
                    "SY",
                    "TH",
                    "TN",
                    "TR",
                    "TT",
                    "TW",
                    "UA",
                    "US",
                    "UY",
                    "UZ",
                    "VA",
                    "VE",
                    "VI",
                    "VN",
                    "YE",
                    "ZA",
                    "ZW",
                ],
            ),
            rx_power_min=dict(required=False, type="int"),
            supported_data_rates=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    radio_profile = NautobotWirelessModule(module, NB_RADIO_PROFILES)
    radio_profile.run()


if __name__ == "__main__":  # pragma: no cover
    main()
