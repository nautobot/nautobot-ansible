# Copyright (c) 2021, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
name: gql_inventory
author:
  - Network to Code (@networktocode)
  - Armen Martirosyan (@armartirosyan)
short_description: Nautobot inventory source using GraphQL capability
description:
  - Get inventory hosts from Nautobot using GraphQL queries
requirements:
  - netutils
options:
  plugin:
    description: Setting that ensures this is a source file for the 'networktocode.nautobot' plugin.
    required: True
    choices: ["networktocode.nautobot.gql_inventory"]
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
    choices: ["urllib2", "all", "yes", "safe", "none"]
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
      - GraphQL query parameters or filters to send to Nautobot to obtain desired data
    type: dict
    default: {}
    suboptions:
      devices:
        description:
          - Additional query parameters or filters for devices
        type: dict
        required: false
      virtual_machines:
        description:
          - Additional query parameters or filters for VMs
        type: dict
        required: false
  group_by:
    required: False
    description:
      - List of dot-sparated paths to index graphql query results (e.g. `platform.slug`)
      - The final value returned by each path is used to derive group names and then group the devices into these groups.
      - Valid group names must be string, so indexing the dotted path should return a string (i.e. `platform.slug` instead of `platform`)
      - > 
          If value returned by the defined path is a dictionary, an attempt will first be made to access the `name` field, and then the `slug` field.
          (i.e. `platform` would attempt to lookup `platform.name`, and if that data was not returned, it would then try `platform.slug`)
    type: list
    elements: str
    default: []
"""

EXAMPLES = """
# inventory.yml file in YAML format
# Example command line: ansible-inventory -v --list -i inventory.yml
# Add -vvv to the command to also see the GraphQL query that gets sent in the debug output.
# Add -vvvv to the command to also see the JSON response that comes back in the debug output.

# Minimum required parameters
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000  # Can be omitted if the NAUTOBOT_URL environment variable is set
token: 1234567890123456478901234567  # Can be omitted if the NAUTOBOT_TOKEN environment variable is set

# This will send the default GraphQL query of:
# query {
#   devices {
#     name
#     primary_ip4 {
#       host
#     }
#     platform {
#       napalm_driver
#     }
#   }
#   virtual_machines {
#     name
#     primary_ip4 {
#       host
#     }
#     platform {
#       name
#     }
#   }
# }

# This module will automatically add the ansible_host key and set it equal to primary_ip4.host
# as well as the ansible_network_os key and set it to platform.napalm_driver
# if the primary_ip4.host and platform.napalm_driver are present on the device in Nautobot.

# Add additional query parameters with the query key.
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  devices:
    tags: name
    serial:
    tenant: name
    site:
      name:
      contact_name:
      description:
      region: name
  virtual_machines:
    tags: name
    tenant: name

# To group by use group_by key
# Specify the full path to the data you would like to use to group by.
# Ensure all paths are also included in the query.
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  devices:
    tags: name
    serial:
    tenant: name
    status: slug
    site:
      name:
      contact_name:
      description:
      region: name
  virtual_machines:
    tags: name
    tenant: name
    status: slug
group_by:
  - tenant.name
  - status.slug

# Filter output using any supported parameters.
# To get supported parameters check the api/docs page for devices.
# Add `filters` to any level of the dictionary and a filter will be added to the GraphQL query at that level.
# (use -vvv to see the underlying GraphQL query being sent)
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  devices:
    filters:
      name__ic: ams
    interfaces:
      filters:
        name__ic: ethernet
      name:
      ip_addresses: address

# You can filter to just devices/virtual_machines by filtering the opposite type to a name that doesn't exist.
# For example, to only get devices:
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  virtual_machines:
    filters:
      name: EXCLUDE ALL
"""

RETURN = """
  _list:
    description:
      - list of composed dictionaries with key and value
    type: list
"""
from collections.abc import Mapping
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
            if not device["primary_ip4"].get("host"):
                self.display.error("Mapping ansible_host requires primary_ip4.host as part of the query.")
                self.add_variable(device["name"], device["name"], "ansible_host")
                return
            self.add_variable(device["name"], device["primary_ip4"]["host"], "ansible_host")
        else:
            self.add_variable(device["name"], device["name"], "ansible_host")

    def add_ansible_platform(self, device):
        """Add network platform to host"""
        if device.get("platform") and "napalm_driver" in device["platform"]:
            self.add_variable(
                device["name"],
                ANSIBLE_LIB_MAPPER_REVERSE.get(NAPALM_LIB_MAPPER.get(device["platform"]["napalm_driver"])),  # Convert napalm_driver to ansible_network_os value
                "ansible_network_os",
            )

    def populate_variables(self, device):
        """Add specified variables to device."""
        for var in device:
            if device[var]:
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

            if not group_name:
                # If the value is empty, it can't be grouped
                continue

            if isinstance(group_name, str):
                # If using force_valid_group_names=always in ansible.cfg, hyphens in Nautobot slugs will be converted to underscores
                group = self.inventory.add_group(group_name)
                self.inventory.add_child(group, device_name)
            else:
                self.display.display(
                    f"Groups must be a string. {group_name} is not a string. Please make sure your group_by path specified resolves to a string value."
                )

    def main(self):
        """Main function."""
        if not HAS_NETUTILS:
            raise AnsibleError("networktocode.nautobot.gql_inventory requires netutils. Please pip install netutils.")

        base_query = {
            "query": {
                "devices": {
                    "name": None,
                    "primary_ip4": "host",
                    "platform": "napalm_driver",
                },
                "virtual_machines": {
                    "name": None,
                    "primary_ip4": "host",
                    "platform": "name",
                },
            }
        }
        if self.gql_query.get("devices"):
            base_query["query"]["devices"].update(self.gql_query["devices"])
        if self.gql_query.get("virtual_machines"):
            base_query["query"]["virtual_machines"].update(self.gql_query["virtual_machines"])
        query = convert_to_graphql_string(base_query)
        data = {"query": query}
        self.display.vvv(f"GraphQL query:\n{query}")

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
        self.display.vvvv(f"JSON response: {json_data}")

        # Error handling in case of a malformed query
        if "errors" in json_data:
            self.display.display(
                "Query returned an error.\nReason: {0}".format(json_data["errors"][0]["message"]),
                color="red",
            )
            # Need to return mock response data that is empty to prevent any failures downstream
            return {"results": [], "next": None}

        for device in json_data["data"].get("devices", []) + json_data["data"].get("virtual_machines", []):
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
        self.follow_redirects = self.get_option("follow_redirects")

        self.main()
