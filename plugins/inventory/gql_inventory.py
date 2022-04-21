# Copyright (c) 2021, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from collections.abc import Mapping

__metaclass__ = type

DOCUMENTATION = """
    name: gql_inventory
    plugin_type: inventory
    author:
      - Armen Martirosyan
    short_description: Nautobot inventory source using GraphQL capability
    description:
      - Get inventory hosts from Nautobot using GraphQL queries
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
      follow_redirects:
          description:
              - Determine how redirects are followed.
              - By default, I(follow_redirects) is set to uses urllib2 default behavior.
          default: urllib2
          choices: ['urllib2', 'all', 'yes', 'safe', 'none']
      validate_certs:
          description:
              - Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted.
          default: True
          type: boolean
      token:
          required: True
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
            - List of dot-sparated paths to index graphql query results (e.g. `platform.slug`)
            - The final value returned by each path is used to derive group names and then group the devices into these groups.
            - Valid group names must be string, so indexing the dotted path should return a string (i.e. `platform.slug` instead of `platform`)
            - If value returned by the defined path is a dictionary, an attempt will first be made to access the `name` field, and then the `slug` field. (i.e. `platform` would attempt to lookup `platform.name`, and if that data was not returned, it would then try `platform.slug`)
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

# Add additional query parameter with query key and use filters
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
query:
  tags: name
  serial:
  site:
    filters:
      tenant: "den"
    name:
    description:
    contact_name:
    description:
    region:
        name:

# To group by use group_by key
# Specify the full path to the data you would like to use to group by.
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
validate_certs: True
group_by:
  - tenant.name
  - status.slug

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
from ansible.module_utils.urls import open_url

from ansible.module_utils.six.moves.urllib import error as urllib_error

from ansible_collections.networktocode.nautobot.plugins.filter.graphql import convert_to_graphql_string

try:
    from netutils.lib_mapper import ANSIBLE_LIB_MAPPER_REVERSE, NAPALM_LIB_MAPPER

    HAS_NETUTILS = True
except ImportError:
    HAS_NETUTILS = False

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

    def add_variable(self, host: str, var: str, var_type: str):
        """Adds variables to group or host.

        Args:
            host (str): Hostname
            var (str): Variable value
            var_type (str): Variable type
        """
        self.inventory.set_variable(host, var_type, var)

    def add_ipv4_address(self, device):
        """Add primary IPv4 address to host."""
        if device["primary_ip4"]:
            self.add_variable(device["name"], device["primary_ip4"]["host"], "ansible_host")
        else:
            self.add_variable(device["name"], device["name"], "ansible_host")

    def add_ansible_platform(self, device):
        """Add network platform to host"""
        if device["platform"] and "napalm_driver" in device["platform"]:
            self.add_variable(
                device["name"],
                ANSIBLE_LIB_MAPPER_REVERSE.get(NAPALM_LIB_MAPPER.get(device["platform"]["napalm_driver"])),  # Convert napalm_driver to ansible_network_os value
                "ansible_network_os",
            )

    def populate_variables(self, device):
        """Add specified variables to device."""
        for var in self.variables:
            if var in device and device[var]:
                self.add_variable(device["name"], device[var], var)

    def create_groups(self, device):
        """Create groups specified and add device to group."""
        device_name = device["name"]
        for group_by_path in self.group_by:
            parent_attr, *chain = group_by_path.split(".")
            device_attr = device.get(parent_attr)
            if device_attr is None:
                self.display.display(f"Could not find value for {parent_attr} on device {device_name}")
                continue

            if not chain:
                group_name = device_attr

            while chain:
                group_name = chain.pop(0)
                if isinstance(device_attr.get(group_name), Mapping):
                    device_attr = device_attr.get(group_name)
                    continue
                else:
                    try:
                        group_name = device_attr[group_name]
                    except KeyError:
                        self.display.display(f"Could not find value for {group_name} in {group_by_path} on device {device_name}.")
                        break

            if isinstance(group_name, Mapping):
                if "name" in group_name:
                    group_name = group_name["name"]
                elif "slug" in group_name:
                    group_name = group_name["slug"]
                else:
                    self.display.display(f"No slug or name value for {group_name} in {group_by_path} on device {device_name}.")

            if isinstance(group_name, str):
                self.inventory.add_group(group_name)
                self.inventory.add_child(group_name, device_name)
            else:
                self.display.display(
                    f"Groups must be a string. {group_name} is not a string. Please make sure your group_by path specified resolves to a string value."
                )

    def main(self):
        """Main function."""
        if not HAS_NETUTILS:
            raise AnsibleError("networktocode.nautobot.gql_inventory requires netutils. Please pip install netutils.")

        self.display.display(msg="In 4.0 the GQL inventory will require changes. Please see release notes for 4.0.0 when available.")

        base_query = {
            "query": {
                "devices": {
                    "name": None,
                    "platform": "napalm_driver",
                    "status": "name",
                    "primary_ip4": "host",
                    "device_role": "name",
                    "site": "name",
                }
            }
        }
        base_query["query"]["devices"].update(self.gql_query)
        if self.filters:
            base_query["query"]["devices"]["filters"] = self.filters
        query = convert_to_graphql_string(base_query)
        data = {"query": query}

        try:
            response = open_url(
                self.api_endpoint + "/api/graphql/",
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
                    "Permission denied: {0}. This may impair functionality of the inventory plugin.".format(self.api_endpoint + "/"),
                    color="red",
                )
                # Need to return mock response data that is empty to prevent any failures downstream
                return {"results": [], "next": None}
            else:
                self.display.display(f"{e.code}", color="red")
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
                "Query returned an error.\nReason: {0}".format(json_data["errors"][0]["message"]),
                color="red",
            )
            # Need to return mock response data that is empty to prevent any failures downstream
            return {"results": [], "next": None}

        for device in json_data["data"]["devices"]:
            self.inventory.add_host(device["name"])
            self.add_ipv4_address(device)
            self.add_ansible_platform(device)
            self.populate_variables(device)
            self.create_groups(device)

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
            "User-Agent": "ansible %s Python %s" % (ansible_version, python_version.split(" ", maxsplit=1)[0]),
            "Content-type": "application/json",
        }
        if token:
            self.headers.update({"Authorization": "Token %s" % token})

        self.gql_query = self.get_option("query")
        self.group_by = self.get_option("group_by")
        self.filters = self.get_option("filters")
        self.variables = self.get_option("additional_variables")
        self.follow_redirects = self.get_option("follow_redirects")

        self.main()
