"""
A lookup function designed to return data from the Nautobot GraphQL endpoint
"""

from __future__ import absolute_import, division, print_function

import os

from ansible.plugins.lookup import LookupBase
from ..module_utils.utils import NautobotApiBase, NautobotGraphQL

__metaclass__ = type

DOCUMENTATION = """
    lookup: lookup
    author: Josh VanDeraa (@jvanderaa)
    version_added: "1.1.0"
    short_description: Queries and returns elements from Nautobot GraphQL endpoint
    description:
        - Queries Nautobot via its GraphQL API through pynautobot
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
                - name: NAUTOBOT_API_TOKEN
            required: False
        url:
            description:
                - The URL to the Nautobot instance to query (http://nautobot.example.com:8000)
            env:
                # in order of precedence
                - name: NAUTOBOT_URL
                - name: NAUTOBOT_API
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
    requirements:
        - pynautobot
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
  - name: Obtain list of devices from Nautobot
    set_fact
      query_response: "{{ query('networktocode.nautobot.lookup_graphql', query=query, url='https://nautobot.example.com', token='<redact>') }}"

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
  - name: Obtain list of devices from Nautobot
    set_fact
      query_response: "{{ query('networktocode.nautobot.lookup_graphql', query=query, variables=variables url='https://nautobot.example.com', token='<redact>') }}"
"""

RETURN = """
  data:
    description:
      - Data result from the GraphQL endpoint
    type: dict
"""


class LookupModule(LookupBase):
    """
    LookupModule(LookupBase) is defined by Ansible
    """

    def run(self, **kwargs):
        # Setup API Token information, URL, and SSL verification
        token = kwargs.get("token") or os.getenv("NAUTOBOT_TOKEN")
        url = kwargs.get("url") or os.getenv("NAUTOBOT_URL")
        ssl_verify = kwargs.get("validate_certs", True)
        nautobot_api = NautobotApiBase(token=token, url=url, ssl_verify=ssl_verify)
        query = kwargs.get("query")
        variables = kwargs.get("variables")

        # Setup return results
        results = {}
        # Make call to Nautobot API and capture any failures
        nautobot_graph_obj = NautobotGraphQL(
            query=query, api=nautobot_api, variables=variables
        )

        # Add data for the return
        results["data"] = nautobot_graph_obj.query()

        # Results should be the data response of the query to be returned as a lookup
        return results
