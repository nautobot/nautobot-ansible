# Copyright (c) 2018 Remy Leone
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
        - Get inventory hosts from Nautobot unsing GraphQL queries
    extends_documentation_fragment:
        - constructed
        - inventory_cache
    options:
        plugin:
            description: Token that ensures this is a source file for the 'nautobot' plugin.
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
        follow_redirects:
            description:
                - Determine how redirects are followed.
                - By default, I(follow_redirects) is set to uses urllib2 default behavior.
            default: urllib2
            choices: ['urllib2', 'all', 'yes', 'safe', 'none']
        max_uri_length:
            description:
                - When fetch_all is False, GET requests to Nautobot may become quite long and return a HTTP 414 (URI Too Long).
                - You can adjust this option to be smaller to avoid 414 errors, or larger for a reduced number of requests.
            type: int
            default: 4000
            version_added: "1.0.0"
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
        variables:
            required: False
            description:
              - Variable types and values to use while making the call
            type: dict
        group_by:
            required: False
            description:
              - List of group names to group the hosts
            type: list
            default: False
"""

EXAMPLES = """
# inventory.yml file in YAML format
# Example command line: ansible-inventory -v --list -i inventory.yml

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

    @property
    def default_query(self):
        """Returns default query"""
        return "devices { name platform { napalm_driver } status { name } primary_ip4 { address } device_role { name } site { name }  cf_port {name}}"

    def create_inventory(self, group: str, host: str, var: str, var_type: str):
        """Creates Ansible inventory.

        Args:
            group (str): Name of the group
            host (str): Hostname
            var (str): Variable value
            var_type (str): Type of the variable
        """
        self.inventory.add_group(group)
        self.inventory.add_host(host, group)
        self.inventory.set_variable(host, var_type, var)

    def main(self):
        """Main function."""
        file_loader = FileSystemLoader(f"{PATH}/../templates")
        env = Environment(loader=file_loader)
        template = env.get_template("graphql_query.j2")
        a = self.gql_query
        query = template.render(query=self.gql_query)

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
                    "Something went wrong while executing the query.\nReturned code: {code}\nReason: {reason}".format(
                        code=e.code, reason=e
                    ),
                    color="red",
                )
                # Need to return mock response data that is empty to prevent any failures downstream
                return {"results": [], "next": None}
        json_data = json.loads(response.read())

        groups = []
        if self.group_by:
            for group_by in self.group_by:
                for device in json_data["data"]["devices"]:
                    if device.get(group_by) and GROUP_BY.get(group_by):
                        if device[group_by][GROUP_BY.get(group_by)] not in groups:
                            groups.append(
                                {device[group_by][GROUP_BY.get(group_by)]: group_by}
                            )
                    else:
                        groups.append({"unknown": "unknown"})

        else:
            for device in json_data["data"]["devices"]:
                groups.append(device["site"]["name"])
                groups.append(device["device_role"]["name"])
                if device["platform"]:
                    groups.append(device["platform"]["name"])

        for group in groups:
            for key, value in group.items():
                for device in json_data["data"]["devices"]:
                    if value in device and device[value]:
                        if key == device[value][GROUP_BY[value]]:
                            if device["primary_ip4"]:
                                self.create_inventory(
                                    key,
                                    device["name"],
                                    device["primary_ip4"]["address"],
                                    "ansible_host",
                                )
                            else:
                                self.create_inventory(
                                    key, device["name"], device["name"], "ansible_host"
                                )

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
        self.follow_redirects = self.get_option("follow_redirects")
        self.max_uri_length = self.get_option("max_uri_length")
        self.headers = {
            "User-Agent": "ansible %s Python %s"
            % (ansible_version, python_version.split(" ")[0]),
            "Content-type": "application/json",
        }
        if token:
            self.headers.update({"Authorization": "Token %s" % token})
        self.gql_query = self.get_option("query")
        self.group_by = self.get_option("group_by")

        self.main()
