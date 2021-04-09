import os

from ansible.errors import AnsibleError
import requests
import pynautobot


class NautobotGraphql:
    """Module to support GraphQL queries in lookup and action modules."""

    def __init__(self, query, variables=None, url=None, token=None, ssl_verify=True):
        self.query = query
        self.variables = variables
        self.url = url or os.getenv("NAUTOBOT_URL") or os.getenv("NAUTOBOT_API")
        self.token = (
            token or os.getenv("NAUTOBOT_TOKEN") or os.getenv("NAUTOBOT_API_TOKEN")
        )
        self._ssl_verify = ssl_verify
        self.session = requests.Session()
        self.verify_required()
        self.query()

    def verify_required(self):
        # Verify the URL is passed in
        if self.url is None:
            raise AnsibleError("Missing required URL connection")

        # Check that Query is passed
        if self.query is None:
            raise AnsibleError(
                "Query parameter was not passed. Please verify that query is passed."
            )

        # Validate that the query passed is of type string
        if not isinstance(self.query, str):
            raise AnsibleError(
                "Query parameter must be of type string. Please see docs for examples."
            )

        # Verify that the variables passed in, if they are passed in are of type dict
        if self.variables is not None and not isinstance(self.variables, dict):
            raise AnsibleError(
                "Variables parameter must be of key/value pairs. Please see docs for examples."
            )

    def query(self):
        # Create Nautobot instance and assign the session
        self.session.verify = self.ssl_verify
        self.nautobot = pynautobot.api(url=self.url, token=self.token)
        self.nautobot.http_session = self.session

        results = dict()
        # Make call to Nautobot API and capture any failures
        graph_response = self.nautobot.graphql.query(
            query=self.query, variables=self.variables
        )

        # Handle for errors in the GraphQL
        if isinstance(graph_response, pynautobot.GraphQLException):
            raise AnsibleError(
                "Error in the query to the Nautobot host. Errors: %s"
                % (graph_response.errors)
            )

        # Successful POST to the API
        if isinstance(graph_response, pynautobot.GraphQLRecord):
            # Build the results
            results["data"] = graph_response.json.get("data")

            return results

        raise AnsibleError("Failed in response to Nautobot GraphQL API")
