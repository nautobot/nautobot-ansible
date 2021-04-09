#!/usr/bin/python
"""Ansible plugin definition for query_graphql action plugin."""
from __future__ import absolute_import, division, print_function

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
lookup: lookup
author: Josh VanDeraa (@jvanderaa)
version_added: "1.1.0"
short_description: Queries and returns elements from Nautobot GraphQL endpoint
description:
    - Queries Nautobot via its GraphQL API through pynautobot
requirements:
    - pynautobot
options:
    query:
        description:
            - The GraphQL formatted query string, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details.
        required: True
    token:
        description:
            - The API token created through Nautobot
        env:
            # in order of precedence
            - name: NAUTOBOT_TOKEN
        required: False
    url:
        description:
            - The URL to the Nautobot instance to query (http://nautobot.example.com:8000)
        env:
            # in order of precedence
            - name: NAUTOBOT_URL
        required: True
    validate_certs:
        description:
            - Whether or not to validate SSL of the Nautobot instance
        required: False
        default: True
    variables:
        description:
            - Dictionary of keys/values to pass into the GraphQL query, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details
        required: False
"""

EXAMPLES = """
  # Make API Query without variables
  - name: SET FACT OF STRING
    set_fact:
      query_string: |
        query {
          sites {
            id
            name
            region {
              name
            }
          }
        }

  # Make query to GraphQL Endpoint
  - name: Obtain list of sites from Nautobot
    networktocode.nautobot.query_graphql:
      url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
      token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
      query: "{{ query_string }}"


  # Example with variables
  - name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
    set_fact:
      variables:
        site_name: den
      query_string: |
        query ($site_name:String!) {
            sites (name: $site_name) {
            id
            name
            region {
                name
            }
            }
        }

  # Get Response with variables
  - name: Obtain list of devices at site in variables from Nautobot
    networktocode.nautobot.query_graphql:
      url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
      token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
      query: "{{ query_string }}"
      variables: "{{ variables }}"
"""

RETURN = """
  data:
    description:
      - Data result from the GraphQL endpoint
    type: dict
  url:
    description:
      - Nautobot URL that was supplied for troubleshooting
  query:
    description:
      - Query string that was sent to Nautobot
  variables:
    description:
      - Variables passed in
"""
from ansible.module_utils.basic import AnsibleModule


def main():
    """Main definition of Action Plugin for query_graphql."""
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(changed=False, original_message="", message="")

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=dict(
            query=dict(required=True, type="str", default=None),
            token=dict(required=False, type="str", no_log=True, default=None),
            url=dict(required=False, type="str", default=None),
            validate_certs=dict(required=False, type="bool", default=True),
            variables=dict(required=False, type="dict", default={}),
        ),
        # Set to true as this is a read only API, this may need to change or have significant changes when Mutations are
        # added to the GraphQL endpoint of Nautobot
        supports_check_mode=True,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
