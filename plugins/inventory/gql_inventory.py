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
        - Get inventory hosts from Nautobot
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
gql_query:


# has_primary_ip is a useful way to filter out patch panels and other passive devices

# Query filters are passed directly as an argument to the fetching queries.
# You can repeat tags in the query string.

query_filters:
  - role: server
  - tag: web
  - tag: production

# See the Nautobot documentation at https://nautobot.readthedocs.io/en/latest/api/overview/
# the query_filters work as a logical **OR**
#
# Prefix any custom fields with cf_ and pass the field value with the regular Nautobot query string

query_filters:
  - cf_foo: bar

# Nautobot inventory plugin also supports Constructable semantics
# You can fill your hosts vars using the compose option:

plugin: networktocode.nautobot.inventory
compose:
  foo: last_updated
  bar: display
  nested_variable: rack.display

# You can use keyed_groups to group on properties of devices or VMs.
# NOTE: It's only possible to key off direct items on the device/VM objects.
plugin: networktocode.nautobot.inventory
keyed_groups:
  - prefix: status
    key: status.value
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

    def create_inventory(self, group, host, var, var_type):
        """[summary]

        Args:
            group ([type]): [description]
            host ([type]): [description]
            var ([type]): [description]
            var_type ([type]): [description]
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
        import pdb

        pdb.set_trace()
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
            raise AnsibleError(to_native(e.fp.read()))
        json_data = json.loads(response.read())
        import pdb

        groups = []
        if self.group_by:
            for group_by in self.group_by:
                try:
                    for device in json_data["data"]["devices"]:
                        if device.get(group_by):
                            if device[group_by]["napalm_driver"] not in groups:
                                groups.append(device[group_by]["napalm_driver"])
                        else:
                            groups.append("unknown")
                except:
                    pdb.set_trace()
        else:
            for device in json_data["data"]["devices"]:
                groups.append(device["site"]["name"])
                groups.append(device["device_role"]["name"])
                if device["platform"]:
                    groups.append(device["platform"]["name"])

        for group in groups:
            for device in json_data["data"]["devices"]:
                if group == device["site"]["name"]:
                    if device["primary_ip4"] != None:
                        self.create_inventory(
                            group,
                            device["name"],
                            device["primary_ip4"]["address"],
                            "ansible_host",
                        )
                    else:
                        self.create_inventory(
                            group, device["name"], device["name"], "ansible_host"
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
