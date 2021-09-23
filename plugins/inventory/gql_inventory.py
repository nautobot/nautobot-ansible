# Copyright (c) 2021, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: gql_inventory
    plugin_type: inventory
    author:
      - Armen Martirosyan
    short_description: Nautobot inventory source using GraphQL capability
    description:
      - Get inventory hosts from Nautobot using GraphQL queries
    extends_documentation_fragment:
      - constructed
      - inventory_cache
    requirements:
      - netutils
    options:
      plugin:
          description: Setting that ensures this is a source file for the 'networktocode.nautobot' plugin.
          required: True
          choices: ['networktocode.nautobot.gql_inventory']
      api_endpoint:
          description: Endpoint of the Nautobot API
          required: True
          env:
            - name: NAUTOBOT_URL
      timeout:
          description: Timeout for Nautobot requests in seconds
          type: int
          default: 60
      validate_certs:
          description:
              - Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted.
          default: True
          type: boolean
      token:
          required: False
          description:
            - Nautobot API token to be able to read against Nautobot.
            - This may not be required depending on the Nautobot setup.
          env:
              # in order of precedence
              - name: NAUTOBOT_TOKEN
      query:
          required: False
          description:
            - GraphQL query to send to Nautobot to obtain desired data
          type: dict
          default: {}
      additional_variables:
          required: False
          description:
            - Variable types and values to use while making the call
          type: list
          default: []
      group_by:
          required: False
          description:
            - List of group names to group the hosts
          type: list
          default: []
      filters:
          required: false
          description:
            - Granular device search query
          type: dict
          default: {}
"""

EXAMPLES = """
# inventory.yml file in YAML format
# Example command line: ansible-inventory -v --list -i inventory.yml

# Add additional query parameter with query key
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
query:
  tags: name

# To group by use group_by key
# Supported inputs are platform, status, device_role, site
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
group_by:
  - platform

# To group by use group_by key
# Supported inputs are platform, status, device_role, site
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
group_by:
  - platform


# Add additional variables
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
additional_variables:
  - device_role

# Add additional variables combined with additional query
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
query:
  interfaces: name
additional_variables:
  - interfaces

# Filter output using any supported parameters
# To get supported parameters check the api/docs page for devices
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
filters:
  name__ic: nym01-leaf-01
  site: nym01
"""

import json
import os
from sys import version as python_version
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.module_utils.ansible_release import __version__ as ansible_version
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.module_utils.urls import open_url

from ansible.module_utils.six.moves.urllib import error as urllib_error
from jinja2 import Environment, FileSystemLoader
from netutils.lib_mapper import ANSIBLE_LIB_MAPPER_REVERSE, NAPALM_LIB_MAPPER

PATH = os.path.dirname(os.path.realpath(__file__))
GROUP_BY = {
    "platform": "napalm_driver",
    "status": "name",
    "device_role": "name",
    "site": "name",
}


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "networktocode.nautobot.gql_inventory"

    def verify_file(self, path):
        """Return true/false if this is possibly a valid file for this plugin to consume."""
        if super(InventoryModule, self).verify_file(path):
            # Base class verifies that file exists and is readable by current user
            if path.endswith((".yml", ".yaml")):
                return True

        return False

    def create_inventory(self, group: str, host: str):
        """Creates Ansible inventory.

        Args:
            group (str): Name of the group
            host (str): Hostname
        """
        self.inventory.add_group(group)
        self.inventory.add_host(host, group)

    def add_variable(self, host: str, var: str, var_type: str):
        """Adds variables to group or host.

        Args:
            host (str): Hostname
            var (str): Variable value
            var_type (str): Variable type
        """
        self.inventory.set_variable(host, var_type, var)

    def main(self):
        """Main function."""
        file_loader = FileSystemLoader(f"{PATH}/../templates")
        env = Environment(loader=file_loader, autoescape=True)
        template = env.get_template("graphql_default_query.j2")
        query = template.render(query=self.gql_query, filters=self.filters)
        data = {"query": "query {%s}" % query}

        try:
            response = open_url(
                self.api_endpoint + "/",
                method="post",
                data=json.dumps(data),
                headers=self.headers,
                timeout=self.timeout,
                validate_certs=self.validate_certs,
                follow_redirects=self.follow_redirects,
            )
        except urllib_error.HTTPError as e:
            """This will return the response body when we encounter an error.
            This is to help determine what might be the issue when encountering an error.
            Please check issue #294 for more info.
            """
            # Prevent inventory from failing completely if the token does not have the proper permissions for specific URLs
            if e.code == 403:
                self.display.display(
                    "Permission denied: {0}. This may impair functionality of the inventory plugin.".format(
                        self.api_endpoint + "/"
                    ),
                    color="red",
                )
                # Need to return mock response data that is empty to prevent any failures downstream
                return {"results": [], "next": None}
            else:
                self.display.display(
                    "Something went wrong while executing the query.\nReason: {reason}".format(
                        reason=json.loads(e.fp.read().decode())["errors"][0]["message"],
                    ),
                    color="red",
                )
                # Need to return mock response data that is empty to prevent any failures downstream
                return {"results": [], "next": None}
        json_data = json.loads(response.read())

        # Error handling in case of a malformed query
        if "errors" in json_data:
            self.display.display(
                "Query returned an error.\nReason: {0}".format(
                    json_data["errors"][0]["message"]
                ),
                color="red",
            )
            # Need to return mock response data that is empty to prevent any failures downstream
            return {"results": [], "next": None}

        groups = {}
        if self.group_by:
            for group_by in self.group_by:
                if not GROUP_BY.get(group_by):
                    self.display.display(
                        "WARNING: '{0}' is not supported as a 'group_by' option. Supported options are: {1} ".format(
                            group_by,
                            " ".join("'{0}',".format(str(x)) for x in GROUP_BY.keys()),
                        ),
                        color="yellow",
                    )
                    continue
                for device in json_data["data"]["devices"]:
                    groups[device["site"]["name"]] = "site"
                    if device.get(group_by) and GROUP_BY.get(group_by):
                        groups[device[group_by][GROUP_BY.get(group_by)]] = group_by
                    else:
                        groups["unknown"] = "unknown"

        else:
            for device in json_data["data"]["devices"]:
                groups[device["site"]["name"]] = "site"

        for key, value in groups.items():
            for device in json_data["data"]["devices"]:
                if device.get(value) and key == device[value][GROUP_BY[value]]:
                    self.create_inventory(key, device["name"])
                    if device["primary_ip4"]:
                        self.add_variable(
                            device["name"],
                            device["primary_ip4"]["address"],
                            "ansible_host",
                        )
                    else:
                        self.add_variable(
                            device["name"], device["name"], "ansible_host"
                        )
                    if device["platform"] and "napalm_driver" in device["platform"]:
                        self.add_variable(
                            device["name"],
                            ANSIBLE_LIB_MAPPER_REVERSE.get(
                                NAPALM_LIB_MAPPER.get(
                                    device["platform"][
                                        "napalm_driver"
                                    ]  # Convert napalm_driver to ansible_network_os value
                                )
                            ),
                            "ansible_network_os",
                        )

                    for var in self.variables:
                        if var in device and device[var]:
                            self.add_variable(device["name"], device[var], var)

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path=path)
        self.use_cache = cache

        # Nautobot access
        token = self.get_option("token")
        # Handle extra "/" from api_endpoint configuration and trim if necessary, see PR#49943
        self.api_endpoint = self.get_option("api_endpoint").strip("/")
        self.validate_certs = self.get_option("validate_certs")
        self.timeout = self.get_option("timeout")
        self.headers = {
            "User-Agent": "ansible %s Python %s"
            % (ansible_version, python_version.split(" ")[0]),
            "Content-type": "application/json",
        }
        if token:
            self.headers.update({"Authorization": "Token %s" % token})

        self.gql_query = self.get_option("query")
        self.group_by = self.get_option("group_by")
        self.filters = self.get_option("filters")
        self.variables = self.get_option("additional_variables")

        self.main()
