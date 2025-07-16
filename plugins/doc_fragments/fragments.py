# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    """Doc Fragments for Ansible Modules."""

    BASE = r"""
requirements:
  - pynautobot
options:
  url:
    description:
      - "The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000)"
      - "Can be omitted if the E(NAUTOBOT_URL) environment variable is configured."
    required: true
    type: str
  token:
    description:
      - "The token created within Nautobot to authorize API access"
      - "Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured."
    required: true
    type: str
  state:
    description:
      - "Use C(present) or C(absent) for adding or removing."
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    version_added: "3.0.0"
    description:
      - "This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined"
      - "in plugins/module_utils/utils.py and provides control to users on what may make"
      - "an object unique in their environment."
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - "If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates."
      - "Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured."
    required: false
    default: true
    type: raw
  api_version:
    version_added: "4.1.0"
    description:
      - "API Version Nautobot REST API"
    required: false
    type: str
"""

    ID = r"""
options:
  id:
    description:
      - "The UUID of the object to operate on"
    required: false
    type: str
    version_added: "5.13.0"
"""

    TAGS = r"""
options:
  tags:
    description:
      - "Any tags that this item may need to be associated with"
    required: false
    type: list
    elements: raw
    version_added: "3.0.0"
"""

    CUSTOM_FIELDS = r"""
options:
  custom_fields:
    description:
      - "Must exist in Nautobot and in key/value format"
    required: false
    type: dict
    version_added: "3.0.0"
"""
