"""
A lookup function designed to return data from the Nautobot GraphQL endpoint
"""

from __future__ import absolute_import, division, print_function

import os

from ansible.errors import AnsibleError, 
from ansible.plugins.lookup import LookupBase


from ansible_collections.networktocode.nautobot.plugins.graphql import NautobotGraphql

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
  errors:
    description:
      - Errors returned on a query
    type: dict
"""


class LookupModule(LookupBase):
    """
    LookupModule(LookupBase) is defined by Ansible
    """

    def run(self, **kwargs):

        # Setup API Token information, URL, and SSL verification
        token = (
            kwargs.get("token")
            or os.getenv("NAUTOBOT_TOKEN")
            or os.getenv("NAUTOBOT_API_TOKEN")
        )
        url = (
            kwargs.get("url") or os.getenv("NAUTOBOT_URL") or os.getenv("NAUTOBOT_API")
        )
        ssl_verify = kwargs.get("validate_certs", True)
        query = kwargs.get("query")
        variables = kwargs.get("variables")

        # Check that Query is passed
        if query is None:
            raise AnsibleError(
                "Query parameter was not passed. Please verify that query is passed."
            )

        # Validate that the query passed is of type string
        if not isinstance(query, str):
            raise AnsibleError(
                "Query parameter must be of type string. Please see docs for examples."
            )

        # Check that variables are passed in are of type dictionary if passed
        if variables is not None and not isinstance(variables, dict):
            raise AnsibleError(
                "Variables parameter must be of key/value pairs. Please see docs for examples."
            )

        # Make call to Nautobot API and capture any failures
        graph_obj = NautobotGraphql()
        results = graph_obj(query=query, variables=variables, url=url, token=token, ssl_verify=ssl_verify)

        # Results should be the data response of the query to be returned as a lookup
        return results
