# Copyright (c) 2018 Remy Leone
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
  name: inventory
  author:
    - Remy Leone (@sieben)
    - Anthony Ruhier (@Anthony25)
    - Nikhil Singh Baliyan (@nikkytub)
    - Sander Steffann (@steffann)
    - Douglas Heriot (@DouglasHeriot)
  short_description: Nautobot inventory source
  description:
    - Get inventory hosts from Nautobot
    - "Note: If gathering an endpoint that has significant number of objects (such as interfaces), you may have failures caused by gathering too much data."
    - "Look to leverage the GraphQL inventory or gather data as a first task in the playbook rather than in inventory."
  extends_documentation_fragment:
    - constructed
    - inventory_cache
  options:
    plugin:
      description: token that ensures this is a source file for the 'nautobot' plugin.
      required: True
      choices: ['networktocode.nautobot.inventory']
    api_endpoint:
      description: Endpoint of the Nautobot API
      required: True
      env:
        - name: NAUTOBOT_URL
    api_version:
      description: The version of the Nautobot REST API.
      required: False
      version_added: "4.1.0"
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
    config_context:
      description:
        - If True, it adds config_context in host vars.
        - Config-context enables the association of arbitrary data to devices and virtual machines grouped by
          location, role, platform, and/or tenant. Please check official nautobot docs for more info.
      default: False
      type: boolean
    flatten_config_context:
      description:
        - If I(config_context) is enabled, by default it's added as a host var named config_context.
        - If flatten_config_context is set to True, the config context variables will be added directly to the host instead.
      default: False
      type: boolean
      version_added: "1.0.0"
    flatten_local_context_data:
      description:
        - If I(local_context_data) is enabled, by default it's added as a host var named local_context_data.
        - If flatten_local_context_data is set to True, the config context variables will be added directly to the host instead.
      default: False
      type: boolean
      version_added: "1.0.0"
    flatten_custom_fields:
      description:
        - By default, host custom fields are added as a dictionary host var named custom_fields.
        - If flatten_custom_fields is set to True, the fields will be added directly to the host instead.
      default: False
      type: boolean
      version_added: "1.0.0"
    token:
      required: False
      description:
        - Nautobot API token to be able to read against Nautobot.
        - This may not be required depending on the Nautobot setup.
      env:
        # in order of precedence
        - name: NAUTOBOT_TOKEN
    plurals:
      description:
        - If True, all host vars are contained inside single-element arrays for legacy compatibility with old versions of this plugin.
        - Group names will be plural (ie. "locations_mylocation" instead of "location_mylocation")
        - The choices of I(group_by) will be changed by this option.
      default: True
      type: boolean
      version_added: "1.0.0"
    interfaces:
      description:
        - If True, it adds the device or virtual machine interface information in host vars.
      default: False
      type: boolean
      version_added: "1.0.0"
    module_interfaces:
      description:
        - If True, it adds module interfaces to the list of device interfaces in the inventory.
        - Modules are only available in Nautobot v2.3.0+
        - Requires I(interfaces) to be enabled as well.
      default: False
      type: boolean
      version_added: "5.12.0"
    services:
      description:
        - If True, it adds the device or virtual machine services information in host vars.
      default: True
      type: boolean
      version_added: "1.0.0"
    fetch_all:
      description:
        - By default, fetching interfaces and services will get all of the contents of Nautobot regardless of query_filters applied to devices and VMs.
        - When set to False, separate requests will be made fetching interfaces, services, and IP addresses for each device_id and virtual_machine_id.
        - If you are using the various query_filters options to reduce the number of devices, querying Nautobot may be faster with fetch_all False.
        - For efficiency, when False, these requests will be batched, for example /api/dcim/interfaces?limit=0&device_id=1&device_id=2&device_id=3
        - These GET request URIs can become quite large for a large number of devices.
        - If you run into HTTP 414 errors, you can adjust the max_uri_length option to suit your web server.
      default: True
      type: boolean
      version_added: "1.0.0"
    group_by:
      description: Keys used to create groups. The I(plurals) option controls which of these are valid.
      type: list
      elements: str
      choices:
        - locations
        - location
        - tenants
        - tenant
        - tenant_group
        - racks
        - rack
        - rack_group
        - rack_role
        - tags
        - tag
        - device_roles
        - role
        - device_types
        - device_type
        - manufacturers
        - manufacturer
        - platforms
        - platform
        - cluster
        - cluster_type
        - cluster_group
        - is_virtual
        - services
        - status
      default: []
    group_names_raw:
      description: Will not add the group_by choice name to the group names
      default: False
      type: boolean
      version_added: "1.0.0"
    query_filters:
      description: List of parameters passed to the query string for both devices and VMs (Multiple values may be separated by commas)
      type: list
      elements: str
      default: []
    device_query_filters:
      description: List of parameters passed to the query string for devices (Multiple values may be separated by commas)
      type: list
      elements: str
      default: []
    vm_query_filters:
      description: List of parameters passed to the query string for VMs (Multiple values may be separated by commas)
      type: list
      elements: str
      default: []
    timeout:
      description: Timeout for Nautobot requests in seconds
      type: int
      default: 60
    max_uri_length:
      description:
        - When fetch_all is False, GET requests to Nautobot may become quite long and return a HTTP 414 (URI Too Long).
        - You can adjust this option to be smaller to avoid 414 errors, or larger for a reduced number of requests.
      type: int
      default: 4000
      version_added: "1.0.0"
    virtual_chassis_name:
      description:
        - When a device is part of a virtual chassis, use the virtual chassis name as the Ansible inventory hostname.
        - The host var values will be from the virtual chassis master.
      type: boolean
      default: False
    dns_name:
      description:
        - Force IP Addresses to be fetched so that the dns_name for the primary_ip of each device or VM is set as a host_var.
        - Setting interfaces will also fetch IP addresses and the dns_name host_var will be set.
      type: boolean
      default: False
    ansible_host_dns_name:
      description:
        - If True, sets DNS Name (fetched from primary_ip) to be used in ansible_host variable, instead of IP Address.
      type: boolean
      default: False
    compose:
      description: List of custom ansible host vars to create from the device object fetched from Nautobot
      default: {}
      type: dict
    rename_variables:
      description:
          - Rename variables evaluated by nb_inventory, before writing them.
          - Each list entry contains a dict with a 'pattern' and a 'repl'.
          - Both 'pattern' and 'repl' are regular expressions.
          - The first matching expression is used, subsequent matches are ignored.
          - Internally `re.sub` is used.
      type: list
      elements: dict
      default: []
"""

EXAMPLES = """
# inventory.yml file in YAML format
# Example command line: ansible-inventory -v --list -i inventory.yml

plugin: networktocode.nautobot.inventory
api_endpoint: http://localhost:8000
validate_certs: true
config_context: false
group_by:
  - device_roles
query_filters:
  - role: network-edge-router
device_query_filters:
  - has_primary_ip: 'true'

# has_primary_ip is a useful way to filter out patch panels and other passive devices

# Query filters are passed directly as an argument to the fetching queries.
# You can repeat tags in the query string.

query_filters:
  - role: server
  - tag: web
  - tag: production

# See the Nautobot documentation at https://nautobot.readthedocs.io/en/latest/api/overview/
# the query_filters work as a logical **OR**

---
# Prefix any custom fields with cf_ and pass the field value with the regular Nautobot query string

query_filters:
  - cf_foo: bar

---
# Nautobot inventory plugin also supports Constructable semantics
# You can fill your hosts vars using the compose option:

plugin: networktocode.nautobot.inventory
compose:
  foo: last_updated
  bar: display
  nested_variable: rack.display
  # You can also use custom fields on the device or a nested object
  device_owner: custom_fields.device_owner
  ansible_network_os: platforms.custom_fields.ansible_network_os

# You can use keyed_groups to group on properties of devices or VMs.
# NOTE: It's only possible to key off direct items on the device/VM objects.
plugin: networktocode.nautobot.inventory
keyed_groups:
  - prefix: status
    key: status.value

# You can use rename_variables to change variable names before the inventory gets loaded.
rename_variables:
  - pattern: "cluster"
    repl: "nautobot_cluster"
  - pattern: "ansible_host"
    repl: "host"
"""

import json
import math
import re
import uuid
from collections import defaultdict
from functools import partial
from itertools import chain
from sys import version as python_version
from threading import Thread
from typing import Iterable

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.ansible_release import __version__ as ansible_version
from ansible.module_utils.six.moves.urllib import error as urllib_error
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.urls import open_url
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable
from ansible.utils.unsafe_proxy import wrap_var
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    check_needs_wrapping,
)


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "networktocode.nautobot.inventory"

    def _fetch_information(self, url):
        results = None
        cache_key = self.get_cache_key(url)

        # get the user's cache option to see if we should save the cache if it is changing
        user_cache_setting = self.get_option("cache")

        # read if the user has caching enabled and the cache isn't being refreshed
        attempt_to_read_cache = user_cache_setting and self.use_cache

        # attempt to read the cache if inventory isn't being refreshed and the user has caching enabled
        if attempt_to_read_cache:
            try:
                results = self._cache[cache_key]
                need_to_fetch = False
            except KeyError:
                # occurs if the cache_key is not in the cache or if the cache_key expired
                # we need to fetch the URL now
                need_to_fetch = True
        else:
            # not reading from cache so do fetch
            need_to_fetch = True

        if need_to_fetch:
            self.display.v("Fetching: " + url)
            try:
                response = open_url(
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                    validate_certs=self.validate_certs,
                    follow_redirects=self.follow_redirects,
                )
            except urllib_error.HTTPError as err:
                raise AnsibleParserError(to_native(err.fp.read()))

            try:
                raw_data = to_text(response.read(), errors="surrogate_or_strict")
            except UnicodeError:
                raise AnsibleError("Incorrect encoding of fetched payload from Nautobot API.")

            try:
                results = json.loads(raw_data)
            except ValueError:
                raise AnsibleError("Incorrect JSON payload: %s" % raw_data)

            # put result in cache if enabled
            if user_cache_setting:
                self._cache[cache_key] = results

        return results

    def get_resource_list(self, api_url):
        """Retrieves resource list from nautobot API.

        Returns:
           A list of all resource from nautobot API.
        """
        if not api_url:
            raise AnsibleError("Please check API URL in script configuration file.")

        resources = []

        # Handle pagination
        while api_url:
            api_output = self._fetch_information(api_url)
            resources.extend(api_output["results"])
            api_url = api_output["next"]

        return resources

    def get_resource_list_chunked(self, api_url, query_key, query_values):
        # Make an API call for multiple specific IDs, like /api/ipam/ip-addresses?limit=0&device_id=1&device_id=2&device_id=3
        # Drastically cuts down HTTP requests comnpared to 1 request per host, in the case where we don't want to fetch_all

        # Make sure query_values is subscriptable
        if not isinstance(query_values, list):
            query_values = list(query_values)

        def query_string(value, separator="&"):
            return separator + query_key + "=" + str(value)

        # Calculate how many queries we can do per API call to stay within max_url_length
        largest_value = str(max(query_values, default=0))  # values are always id ints
        length_per_value = len(query_string(largest_value))
        chunk_size = math.floor((self.max_uri_length - len(api_url)) / length_per_value)

        # Sanity check, for case where max_uri_length < (api_url + length_per_value)
        if chunk_size < 1:
            chunk_size = 1

        resources = []

        for i in range(0, len(query_values), chunk_size):
            # fmt: off
            chunk = query_values[i: i + chunk_size]
            # fmt: on
            # process chunk of size <= chunk_size
            url = api_url
            for value in chunk:
                url += query_string(value, "&" if "?" in url else "?")

            resources.extend(self.get_resource_list(url))

        return resources

    @property
    def group_extractors(self):
        # List of group_by options and hostvars to extract

        # Some keys are different depending on plurals option
        extractors = {
            "disk": self.extract_disk,
            "memory": self.extract_memory,
            "vcpus": self.extract_vcpus,
            "status": self.extract_status,
            "config_context": self.extract_config_context,
            "local_context_data": self.extract_local_context_data,
            "custom_fields": self.extract_custom_fields,
            self._pluralize_group_by("location"): self.extract_locations,
            "cluster": self.extract_cluster,
            "cluster_group": self.extract_cluster_group,
            "cluster_type": self.extract_cluster_type,
            "is_virtual": self.extract_is_virtual,
            self._pluralize_group_by("tenant"): self.extract_tenant,
            "tenant_group": self.extract_tenant_group,
            self._pluralize_group_by("rack"): self.extract_rack,
            "rack_group": self.extract_rack_group,
            "rack_role": self.extract_rack_role,
            self._pluralize_group_by("tag"): self.extract_tags,
            self._pluralize_group_by("role"): self.extract_device_role,
            self._pluralize_group_by("platform"): self.extract_platform,
            self._pluralize_group_by("device_type"): self.extract_device_type,
            self._pluralize_group_by("manufacturer"): self.extract_manufacturer,
        }

        if self.services:
            extractors.update({"services": self.extract_services})

        if self.interfaces:
            extractors.update({"interfaces": self.extract_interfaces})

        if self.interfaces or self.dns_name or self.ansible_host_dns_name:
            extractors.update({"dns_name": self.extract_dns_name})

        return extractors

    def _pluralize_group_by(self, group_by):
        mapping = {
            "location": "locations",
            "tenant": "tenants",
            "rack": "racks",
            "tag": "tags",
            "role": "device_roles",
            "platform": "platforms",
            "device_type": "device_types",
            "manufacturer": "manufacturers",
        }

        if self.plurals:
            mapped = mapping.get(group_by)
            return mapped or group_by
        else:
            return group_by

    def _pluralize(self, extracted_value):
        # If plurals is enabled, wrap in a single-element list for backwards compatibility
        if self.plurals:
            return [extracted_value]
        else:
            return extracted_value

    def _objects_array_following_parents(self, initial_object_id, object_lookup, object_parent_lookup):
        objects = []

        object_id = initial_object_id

        # Keep looping until the object has no parent
        while object_id is not None:
            object_name = object_lookup[object_id]

            if object_name in objects:
                # Won't ever happen - defensively guard against infinite loop
                break

            objects.append(object_name)

            # Get the parent of this object
            object_id = object_parent_lookup[object_id]

        return objects

    def extract_disk(self, host):
        return host.get("disk")

    def extract_vcpus(self, host):
        return host.get("vcpus")

    def extract_status(self, host):
        return host["status"]

    def extract_memory(self, host):
        return host.get("memory")

    def extract_platform(self, host):
        try:
            return self._pluralize(self.platforms_lookup[host["platform"]["id"]])
        except Exception:
            return

    def extract_services(self, host):
        try:
            services_lookup = self.vm_services_lookup if host["is_virtual"] else self.device_services_lookup

            return list(services_lookup[host["id"]].values())

        except Exception:
            return

    def extract_device_type(self, host):
        try:
            return self._pluralize(self.device_types_lookup[host["device_type"]["id"]])
        except Exception:
            return

    def extract_rack(self, host):
        try:
            return self._pluralize(self.racks_lookup[host["rack"]["id"]])
        except Exception:
            return

    def extract_rack_group(self, host):
        # A host may have a rack. A rack may have a rack_group. A rack_group may have a parent rack_group.
        # Produce a list of rack_groups:
        # - it will be empty if the device has no rack, or the rack has no rack_group
        # - it will have 1 element if the rack's group has no parent
        # - it will have multiple elements if the rack's group has a parent group

        rack = host.get("rack", None)
        if not isinstance(rack, dict):
            # Device has no rack
            return None

        rack_id = rack.get("id", None)
        if rack_id is None:
            # Device has no rack
            return None

        return self._objects_array_following_parents(
            initial_object_id=self.racks_group_lookup[rack_id],
            object_lookup=self.rack_groups_lookup,
            object_parent_lookup=self.rack_group_parent_lookup,
        )

    def extract_rack_role(self, host):
        try:
            return self.racks_role_lookup[host["rack"]["id"]]
        except Exception:
            return

    def extract_tenant(self, host):
        try:
            return self._pluralize(self.tenants_lookup[host["tenant"]["id"]])
        except Exception:
            return

    def extract_tenant_group(self, host):
        try:
            return self.tenant_group_lookup[host["tenant"]["id"]]
        except Exception:
            return

    def extract_device_role(self, host):
        try:
            return self._pluralize(self.device_roles_lookup[host["role"]["id"]])
        except Exception:
            return

    def extract_config_context(self, host):
        try:
            if self.flatten_config_context:
                # Don't wrap in an array if we're about to flatten it to separate host vars
                return host["config_context"]
            else:
                return self._pluralize(host["config_context"])
        except Exception:
            return

    def extract_local_context_data(self, host):
        try:
            if self.flatten_local_context_data:
                # Don't wrap in an array if we're about to flatten it to separate host vars
                return host["local_config_context_data"]
            else:
                return self._pluralize(host["local_config_context_data"])
        except Exception:
            return

    def extract_manufacturer(self, host):
        try:
            if host["is_virtual"]:
                return self._pluralize(self.manufacturers_lookup[host["platform"]["manufacturer"]["id"]])
            return self._pluralize(self.manufacturers_lookup[host["device_type"]["manufacturer"]["id"]])
        except Exception:
            return

    def extract_primary_ip(self, host):
        address_v4 = self.extract_primary_ip4(host)
        address_v6 = self.extract_primary_ip6(host)
        if address_v4:
            return address_v4
        elif address_v6:
            return address_v6

    def extract_primary_ip4(self, host):
        try:
            return host["primary_ip4"]
        except Exception:
            return

    def extract_primary_ip6(self, host):
        try:
            return host["primary_ip6"]
        except Exception:
            return

    def extract_tags(self, host):
        try:
            tag_zero = host["tags"][0]
            # Check the type of the first element in the "tags" array.
            # If a dictionary (Nautobot >= 2.9), return an array of tags' names.
            if isinstance(tag_zero, dict):
                return list(sub["name"] for sub in host["tags"])
            # If a string (Nautobot <= 2.8), return the original "tags" array.
            elif isinstance(tag_zero, str):
                return host["tags"]
        # If tag_zero fails definition (no tags), return the empty array.
        except Exception:
            return host["tags"]

    def extract_interfaces(self, host):
        try:
            interfaces_lookup = self.vm_interfaces_lookup if host["is_virtual"] else self.device_interfaces_lookup

            interfaces = list(interfaces_lookup[host["id"]].values())

            before_v29 = bool(self.ipaddresses_intf_lookup)
            # Attach IP Addresses to their interface
            for interface in interfaces:
                if before_v29:
                    interface["ip_addresses"] = list(self.ipaddresses_intf_lookup[interface["id"]].values())
                else:
                    interface["ip_addresses"] = list(
                        self.vm_ipaddresses_intf_lookup[interface["id"]].values()
                        if host["is_virtual"]
                        else self.device_ipaddresses_intf_lookup[interface["id"]].values()
                    )

            return interfaces
        except Exception:
            return

    def extract_custom_fields(self, host):
        try:
            return host["custom_fields"]
        except Exception:
            return

    def _extract_location_from_host(self, host):
        if host.get("object_type") == "virtualization.virtualmachine":
            return host.get("cluster", {}).get("location")
        else:
            return host.get("location", None)

    def extract_location(self, host):
        location = self._extract_location_from_host(host)
        if isinstance(location, dict):
            return self.locations_lookup.get(location["id"])

    def extract_locations(self, host):
        # A host may have a location. A location may have a parent location.
        # Produce a list of locations:
        # - it will be empty if the device has no location
        # - it will have 1 element if the location has no parent
        # - it will have multiple elements if the location has a parent location

        location = self._extract_location_from_host(host)

        if not isinstance(location, dict):
            # Device has no location
            return []

        location_id = location.get("id", None)
        if location_id is None:
            # Location doesn't exist
            return []

        return self._objects_array_following_parents(
            initial_object_id=location_id,
            object_lookup=self.locations_lookup,
            object_parent_lookup=self.locations_parent_lookup,
        )

    def extract_cluster(self, host):
        try:
            return host["cluster"]["name"]
        except Exception:
            return

    def extract_cluster_group(self, host):
        try:
            return self.clusters_group_lookup[host["cluster"]["id"]]
        except Exception:
            return

    def extract_cluster_type(self, host):
        try:
            return self.clusters_type_lookup[host["cluster"]["id"]]
        except Exception:
            return

    def extract_is_virtual(self, host):
        return host.get("is_virtual")

    def extract_dns_name(self, host):
        primary_ip = self.extract_primary_ip(host)
        # No primary IP assigned
        if not primary_ip:
            return None

        ip_address = self.ipaddresses_lookup.get(primary_ip["id"])

        # Don"t assign a host_var for empty dns_name
        if ip_address.get("dns_name") == "":
            return None

        return ip_address.get("dns_name")

    def refresh_platforms_lookup(self):
        url = self.api_endpoint + "/api/dcim/platforms/?limit=0"
        platforms = self.get_resource_list(api_url=url)
        self.platforms_lookup = dict((platform["id"], platform["network_driver"]) for platform in platforms)

    def refresh_locations_lookup(self):
        url = self.api_endpoint + "/api/dcim/locations/?limit=0"
        locations = self.get_resource_list(api_url=url)
        self.locations_lookup = dict((location["id"], location["name"]) for location in locations)

        def get_location_parent(location):
            # Will fail if location does not have a parent location
            try:
                return (location["id"], location["parent"]["id"])
            except Exception:
                return (location["id"], None)

        # Dictionary of location id to parent location id
        self.locations_parent_lookup = dict(filter(lambda x: x is not None, map(get_location_parent, locations)))

    def refresh_tenants_lookup(self):
        url = self.api_endpoint + "/api/tenancy/tenants/?limit=0&depth=1"
        tenants = self.get_resource_list(api_url=url)
        self.tenants_lookup = dict((tenant["id"], tenant["name"]) for tenant in tenants)

        def get_group_for_tenant(tenant):
            try:
                return (tenant["id"], tenant["tenant_group"]["name"])
            except Exception:
                return (tenant["id"], None)

        self.tenant_group_lookup = dict(map(get_group_for_tenant, tenants))

    def refresh_racks_lookup(self):
        url = self.api_endpoint + "/api/dcim/racks/?limit=0&depth=1"
        racks = self.get_resource_list(api_url=url)
        self.racks_lookup = dict((rack["id"], rack["name"]) for rack in racks)

        def get_group_for_rack(rack):
            try:
                return (rack["id"], rack["rack_group"]["id"])
            except Exception:
                return (rack["id"], None)

        def get_role_for_rack(rack):
            try:
                return (rack["id"], rack["role"]["name"])
            except Exception:
                return (rack["id"], None)

        self.racks_group_lookup = dict(map(get_group_for_rack, racks))
        self.racks_role_lookup = dict(map(get_role_for_rack, racks))

    def refresh_rack_groups_lookup(self):
        url = self.api_endpoint + "/api/dcim/rack-groups/?limit=0&depth=1"
        rack_groups = self.get_resource_list(api_url=url)
        self.rack_groups_lookup = dict((rack_group["id"], rack_group["name"]) for rack_group in rack_groups)

        def get_rack_group_parent(rack_group):
            try:
                return (rack_group["id"], rack_group["parent"]["id"])
            except Exception:
                return (rack_group["id"], None)

        # Dictionary of rack group id to parent rack group id
        self.rack_group_parent_lookup = dict(map(get_rack_group_parent, rack_groups))

    def refresh_device_roles_lookup(self):
        url = self.api_endpoint + "/api/extras/roles/?limit=0"
        roles = self.get_resource_list(api_url=url)
        self.device_roles_lookup = dict(
            (role["id"], role["name"])
            for role in roles
            if "dcim.device" in role["content_types"] or "virtualization.virtualmachine" in role["content_types"]
        )

    def refresh_device_types_lookup(self):
        url = self.api_endpoint + "/api/dcim/device-types/?limit=0"
        device_types = self.get_resource_list(api_url=url)
        self.device_types_lookup = dict((device_type["id"], device_type["model"]) for device_type in device_types)

    def refresh_manufacturers_lookup(self):
        url = self.api_endpoint + "/api/dcim/manufacturers/?limit=0"
        manufacturers = self.get_resource_list(api_url=url)
        self.manufacturers_lookup = dict((manufacturer["id"], manufacturer["name"]) for manufacturer in manufacturers)

    def refresh_clusters_lookup(self):
        url = self.api_endpoint + "/api/virtualization/clusters/?limit=0&depth=1"
        clusters = self.get_resource_list(api_url=url)

        def get_cluster_type(cluster):
            # Will fail if cluster does not have a type (required property so should always be true)
            try:
                return (cluster["id"], cluster["cluster_type"]["name"])
            except Exception:
                return (cluster["id"], None)

        def get_cluster_group(cluster):
            # Will fail if cluster does not have a group (group is optional)
            try:
                return (cluster["id"], cluster["cluster_group"]["name"])
            except Exception:
                return (cluster["id"], None)

        self.clusters_type_lookup = dict(map(get_cluster_type, clusters))
        self.clusters_group_lookup = dict(map(get_cluster_group, clusters))

    def refresh_services(self):
        url = self.api_endpoint + "/api/ipam/services/?limit=0&depth=1"
        services = []

        if self.fetch_all:
            services = self.get_resource_list(url)
        else:
            device_services = self.get_resource_list_chunked(
                api_url=url,
                query_key="device",
                query_values=self.devices_lookup.keys(),
            )
            vm_services = self.get_resource_list_chunked(
                api_url=url,
                query_key="virtual_machine",
                query_values=self.vms_lookup.keys(),
            )
            services = chain(device_services, vm_services)

        # Construct a dictionary of dictionaries, separately for devices and vms.
        # Allows looking up services by device id or vm id
        self.device_services_lookup = defaultdict(dict)
        self.vm_services_lookup = defaultdict(dict)

        for service in services:
            service_id = service["id"]

            if service.get("device"):
                self.device_services_lookup[service["device"]["id"]][service_id] = service

            if service.get("virtual_machine"):
                self.vm_services_lookup[service["virtual_machine"]["id"]][service_id] = service

    def refresh_interfaces(self):
        # Device information on Parent Module Bays are only available at depth=2
        depth = "2" if self.module_interfaces else "1"
        url_device_interfaces = self.api_endpoint + f"/api/dcim/interfaces/?limit=0&depth={depth}"
        url_vm_interfaces = self.api_endpoint + "/api/virtualization/interfaces/?limit=0&depth=1"

        device_interfaces = []
        vm_interfaces = []

        if self.fetch_all:
            device_interfaces = self.get_resource_list(url_device_interfaces)
            vm_interfaces = self.get_resource_list(url_vm_interfaces)
        else:
            device_interfaces = self.get_resource_list_chunked(
                api_url=url_device_interfaces,
                query_key="device_id",
                query_values=self.devices_lookup.keys(),
            )
            vm_interfaces = self.get_resource_list_chunked(
                api_url=url_vm_interfaces,
                query_key="virtual_machine_id",
                query_values=self.vms_lookup.keys(),
            )

        # Construct a dictionary of dictionaries, separately for devices and vms.
        # For a given device id or vm id, get a lookup of interface id to interface
        # This is because interfaces may be returned multiple times when querying for virtual chassis parent and child in separate queries
        self.device_interfaces_lookup = defaultdict(dict)
        self.vm_interfaces_lookup = defaultdict(dict)

        # /dcim/interfaces gives ip_address_count per interface. /virtualization/interfaces does not
        self.devices_with_ips = set()

        for interface in device_interfaces:
            interface_id = interface["id"]
            if interface.get("device"):
                device_id = interface["device"]["id"]
            elif self.module_interfaces and interface.get("module", {}).get("parent_module_bay", {}).get(
                "parent_device"
            ):
                device_id = interface["module"]["parent_module_bay"]["parent_device"]["id"]
            else:
                continue

            # Check if device_id is actually a device we've fetched, and was not filtered out by query_filters
            if device_id not in self.devices_lookup:
                continue

            # Check if device_id is part of a virtual chasis
            # If so, treat its interfaces as actually part of the master
            device = self.devices_lookup[device_id]
            virtual_chassis_master = self._get_host_virtual_chassis_master(device)
            if virtual_chassis_master is not None:
                device_id = virtual_chassis_master

            self.device_interfaces_lookup[device_id][interface_id] = interface

            # Keep track of what devices have interfaces with IPs, so if fetch_all is False we can avoid unnecessary queries
            if interface["ip_address_count"] > 0:
                self.devices_with_ips.add(device_id)

        for interface in vm_interfaces:
            interface_id = interface["id"]
            vm_id = interface["virtual_machine"]["id"]

            self.vm_interfaces_lookup[vm_id][interface_id] = interface

    # Note: depends on the result of refresh_interfaces for self.devices_with_ips
    def refresh_ipaddresses(self):
        # setting depth=2 to fetch information about namespaces under parent prefixes.
        url = self.api_endpoint + "/api/ipam/ip-addresses/?limit=0&depth=2&has_interface_assignments=true"
        ipaddresses = []

        if self.fetch_all:
            ipaddresses = self.get_resource_list(url)
        else:
            device_ips = self.get_resource_list_chunked(
                api_url=url,
                query_key="device_id",
                query_values=list(self.devices_with_ips),
            )
            vm_ips = self.get_resource_list_chunked(
                api_url=url,
                query_key="virtual_machine_id",
                query_values=self.vms_lookup.keys(),
            )

            ipaddresses = chain(device_ips, vm_ips)

        # Construct a dictionary of lists, to allow looking up ip addresses by interface id
        # Note that interface ids share the same namespace for both devices and vms so this is a single dictionary
        self.ipaddresses_intf_lookup = defaultdict(dict)
        # Construct a dictionary of the IP addresses themselves
        self.ipaddresses_lookup = defaultdict(dict)
        # Nautobot v2.9 and onwards
        self.vm_ipaddresses_intf_lookup = defaultdict(dict)
        self.vm_ipaddresses_lookup = defaultdict(dict)
        self.device_ipaddresses_intf_lookup = defaultdict(dict)
        self.device_ipaddresses_lookup = defaultdict(dict)

        for ipaddress in ipaddresses:
            # We need to copy the ipaddress entry to preserve the original in case caching is used.
            ipaddress_copy = ipaddress.copy()
            ip_id = ipaddress["id"]
            for interface in ipaddress["interfaces"]:
                interface_id = interface["id"]
                self.device_ipaddresses_lookup[ip_id] = ipaddress_copy
                self.device_ipaddresses_intf_lookup[interface_id][ip_id] = ipaddress_copy
                self.ipaddresses_intf_lookup[interface_id][ip_id] = ipaddress_copy
                self.ipaddresses_lookup[ip_id] = ipaddress_copy

            for interface in ipaddress["vm_interfaces"]:
                interface_id = interface["id"]
                self.vm_ipaddresses_lookup[ip_id] = ipaddress_copy
                self.vm_ipaddresses_intf_lookup[interface_id][ip_id] = ipaddress_copy
                self.ipaddresses_intf_lookup[interface_id][ip_id] = ipaddress_copy
                self.ipaddresses_lookup[ip_id] = ipaddress_copy
            # Remove "interface" attribute, as that's redundant when ipaddress is added to an interface
            del ipaddress_copy["interfaces"]
            del ipaddress_copy["vm_interfaces"]

    @property
    def lookup_processes(self):
        lookups = [
            self.refresh_locations_lookup,
            self.refresh_tenants_lookup,
            self.refresh_racks_lookup,
            self.refresh_rack_groups_lookup,
            self.refresh_device_roles_lookup,
            self.refresh_platforms_lookup,
            self.refresh_device_types_lookup,
            self.refresh_manufacturers_lookup,
            self.refresh_clusters_lookup,
        ]

        if self.interfaces:
            lookups.append(self.refresh_interfaces)

        if self.services:
            lookups.append(self.refresh_services)

        return lookups

    @property
    def lookup_processes_secondary(self):
        lookups = []

        # IP addresses are needed for either interfaces or dns_name options
        if self.interfaces or self.dns_name or self.ansible_host_dns_name:
            lookups.append(self.refresh_ipaddresses)

        return lookups

    def refresh_lookups(self, lookups):
        # Exceptions that occur in threads by default are printed to stderr, and ignored by the main thread
        # They need to be caught, and raised in the main thread to prevent further execution of this plugin

        thread_exceptions = []

        def handle_thread_exceptions(lookup):
            def wrapper():
                try:
                    lookup()
                except Exception as e:
                    # Save for the main-thread to re-raise
                    # Also continue to raise on this thread, so the default handler can run to print to stderr
                    thread_exceptions.append(e)
                    raise e

            return wrapper

        thread_list = []

        try:
            for lookup in lookups:
                thread = Thread(target=handle_thread_exceptions(lookup))
                thread_list.append(thread)
                thread.start()

            for thread in thread_list:
                thread.join()

            # Wait till we've joined all threads before raising any exceptions
            for exception in thread_exceptions:
                raise exception

        finally:
            # Avoid retain cycles
            thread_exceptions = None

    def fetch_api_docs(self):
        openapi = self._fetch_information(self.api_endpoint + "/api/docs/?format=openapi")

        device_path = "/api/dcim/devices/" if "/api/dcim/devices/" in openapi["paths"] else "/dcim/devices/"
        vm_path = (
            "/api/virtualization/virtual-machines/"
            if "/api/virtualization/virtual-machines/" in openapi["paths"]
            else "/virtualization/virtual-machines/"
        )

        self.allowed_device_query_parameters = [p["name"] for p in openapi["paths"][device_path]["get"]["parameters"]]
        self.allowed_vm_query_parameters = [p["name"] for p in openapi["paths"][vm_path]["get"]["parameters"]]

    def validate_query_parameter(self, parameter, allowed_query_parameters):
        if not (isinstance(parameter, dict) and len(parameter) == 1):
            self.display.warning("Warning query parameters %s not a dict with a single key." % parameter)
            return None

        k = tuple(parameter.keys())[0]
        v = tuple(parameter.values())[0]

        if not (k in allowed_query_parameters or k.startswith("cf_")):
            msg = "Warning: %s not in %s or starting with cf (Custom field)" % (
                k,
                allowed_query_parameters,
            )
            self.display.warning(msg=msg)
            return None
        return k, v

    def filter_query_parameters(self, parameters, allowed_query_parameters):
        return filter(
            lambda parameter: parameter is not None,
            # For each element of query_filters, test if it's allowed
            map(
                # Create a partial function with the device-specific list of query parameters
                partial(
                    self.validate_query_parameter,
                    allowed_query_parameters=allowed_query_parameters,
                ),
                parameters,
            ),
        )

    def refresh_url(self):
        device_query_parameters = [("limit", 0), ("depth", 1)]
        vm_query_parameters = [("limit", 0), ("depth", 1)]
        device_url = self.api_endpoint + "/api/dcim/devices/?"
        vm_url = self.api_endpoint + "/api/virtualization/virtual-machines/?"

        # Add query_filtes to both devices and vms query, if they're valid
        if isinstance(self.query_filters, Iterable):
            device_query_parameters.extend(
                self.filter_query_parameters(self.query_filters, self.allowed_device_query_parameters)
            )

            vm_query_parameters.extend(
                self.filter_query_parameters(self.query_filters, self.allowed_vm_query_parameters)
            )

        if isinstance(self.device_query_filters, Iterable):
            device_query_parameters.extend(
                self.filter_query_parameters(self.device_query_filters, self.allowed_device_query_parameters)
            )

        if isinstance(self.vm_query_filters, Iterable):
            vm_query_parameters.extend(
                self.filter_query_parameters(self.vm_query_filters, self.allowed_vm_query_parameters)
            )

        # When query_filters is Iterable, and is not empty:
        # - If none of the filters are valid for devices, do not fetch any devices
        # - If none of the filters are valid for VMs, do not fetch any VMs
        # If either device_query_filters or vm_query_filters are set,
        # device_query_parameters and vm_query_parameters will have > 1 element so will continue to be requested
        if self.query_filters and isinstance(self.query_filters, Iterable):
            if len(device_query_parameters) <= 1:
                device_url = None

            if len(vm_query_parameters) <= 1:
                vm_url = None

        # Append the parameters to the URLs
        if device_url:
            device_url = device_url + urlencode(device_query_parameters)
        if vm_url:
            vm_url = vm_url + urlencode(vm_query_parameters)

        # Include config_context if required
        if self.config_context:
            if device_url:
                device_url = f"{device_url}&include=config_context"
            if vm_url:
                vm_url = f"{vm_url}&include=config_context"

        return device_url, vm_url

    def fetch_hosts(self):
        device_url, vm_url = self.refresh_url()

        self.devices_list = []
        self.vms_list = []

        if device_url:
            self.devices_list = self.get_resource_list(device_url)

        if vm_url:
            self.vms_list = self.get_resource_list(vm_url)

        # Allow looking up devices/vms by their ids
        self.devices_lookup = {device["id"]: device for device in self.devices_list}
        self.vms_lookup = {vm["id"]: vm for vm in self.vms_list}

        # There's nothing that explicitly says if a host is virtual or not - add in a new field
        for host in self.devices_list:
            host["is_virtual"] = False

        for host in self.vms_list:
            host["is_virtual"] = True

    def extract_name(self, host):
        # An host in an Ansible inventory requires an hostname.
        # name is an unique but not required attribute for a device in Nautobot
        # We default to an UUID for hostname in case the name is not set in Nautobot
        # Use virtual chassis name if set by the user.
        if self.virtual_chassis_name and self._get_host_virtual_chassis_master(host):
            return host["virtual_chassis"]["name"] or str(uuid.uuid4())
        else:
            return host["name"] or str(uuid.uuid4())

    @staticmethod
    def _remove_invalid_group_chars(group):
        # Removes spaces and hyphens which Ansible doesn't like and converts to lowercase.
        return group.replace("-", "_").replace(" ", "_").lower()

    def set_inv_var_safely(self, hostname, variable_name, value):
        """Set inventory variable with conditional wrapping only where needed."""
        if check_needs_wrapping(value):
            value = wrap_var(value)
        self.inventory.set_variable(hostname, variable_name, value)

    def generate_group_name(self, grouping, group):
        # Check for special case - if group is a boolean, just return grouping name instead
        # eg. "is_virtual" - returns true for VMs, should put them in a group named "is_virtual", not "is_virtual_True"
        if isinstance(group, bool):
            if group:
                return grouping
            else:
                # Don't create the inverse group
                return None

        # Special case. Extract name from service, which is a hash.
        if grouping == "services":
            group = group["name"]
            grouping = "service"

        if grouping == "status":
            group = group["display"]

        group = self._remove_invalid_group_chars(group)
        return group if self.group_names_raw else "_".join([grouping, group])

    def add_host_to_groups(self, host, hostname):
        for grouping in self.group_by:
            if grouping not in self.group_extractors:
                raise AnsibleError(
                    'group_by option "%s" is not valid. (Maybe check the plurals option? It can determine what group_by options are valid)'
                    % grouping
                )

            groups_for_host = self.group_extractors[grouping](host)

            if not groups_for_host:
                continue

            # Make groups_for_host a list if it isn't already
            if not isinstance(groups_for_host, list):
                groups_for_host = [groups_for_host]

            for group_for_host in groups_for_host:
                group_name = self.generate_group_name(grouping, group_for_host)

                if not group_name:
                    continue

                # Group names may be transformed by the ansible TRANSFORM_INVALID_GROUP_CHARS setting
                # add_group returns the actual group name used
                transformed_group_name = self.inventory.add_group(group=group_name)
                self.inventory.add_host(group=transformed_group_name, host=hostname)

    def _add_location_groups(self):
        # Mapping of location id to group name
        location_transformed_group_names = dict()

        # Create groups for each location
        for location_id in self.locations_lookup:
            location_group_name = self.generate_group_name("location", self.locations_lookup[location_id])
            location_transformed_group_names[location_id] = self.inventory.add_group(group=location_group_name)

        # Now that all location groups exist, add relationships between them
        for location_id in self.locations_lookup:
            location_group_name = location_transformed_group_names[location_id]
            parent_location_id = self.locations_parent_lookup.get(location_id, None)
            if parent_location_id is not None and parent_location_id in location_transformed_group_names:
                parent_location_name = location_transformed_group_names[parent_location_id]
                self.inventory.add_child(parent_location_name, location_group_name)

    def _set_variable(self, hostname, key, value):
        for item in self.rename_variables:
            if item["pattern"].match(key):
                key = item["pattern"].sub(item["repl"], key)
                break

        self.inventory.set_variable(hostname, key, value)

    def _fill_host_variables(self, host, hostname):
        extracted_primary_ip = self.extract_primary_ip(host=host)
        if extracted_primary_ip:
            self.set_inv_var_safely(hostname, "ansible_host", extracted_primary_ip["host"])

        if self.ansible_host_dns_name:
            extracted_dns_name = self.extract_dns_name(host=host)
            if extracted_dns_name:
                self.set_inv_var_safely(hostname, "ansible_host", extracted_dns_name)

        extracted_primary_ip4 = self.extract_primary_ip4(host=host)
        if extracted_primary_ip4:
            self.set_inv_var_safely(hostname, "primary_ip4", extracted_primary_ip4["host"])

        extracted_primary_ip6 = self.extract_primary_ip6(host=host)
        if extracted_primary_ip6:
            self.set_inv_var_safely(hostname, "primary_ip6", extracted_primary_ip6["host"])

        location = self.extract_location(host=host)
        if location:
            self.set_inv_var_safely(hostname, "location", location)

        for attribute, extractor in self.group_extractors.items():
            extracted_value = extractor(host)

            # Compare with None, not just check for a truth comparison - allow empty arrays, etc to be host vars
            if extracted_value is None:
                continue

            # Special case - all group_by options are single strings, but tag is a list of tags
            # Keep the groups named singular "tag_sometag", but host attribute should be "tags":["sometag", "someothertag"]
            if attribute == "tag":
                attribute = "tags"

            if attribute == "location":
                attribute = "locations"

            if attribute == "rack_group":
                attribute = "rack_groups"

            # Flatten the dict into separate host vars, if enabled
            if isinstance(extracted_value, dict) and (
                (attribute == "config_context" and self.flatten_config_context)
                or (attribute == "custom_fields" and self.flatten_custom_fields)
                or (attribute == "local_config_context_data" and self.flatten_local_context_data)
            ):
                for key, value in extracted_value.items():
                    self.set_inv_var_safely(hostname, key, value)
            else:
                self.set_inv_var_safely(hostname, attribute, extracted_value)

    def _get_host_virtual_chassis_master(self, host):
        virtual_chassis = host.get("virtual_chassis", None)

        if not virtual_chassis:
            return None

        master = virtual_chassis.get("master", None)

        if not master:
            return None

        return master.get("id", None)

    def main(self):
        # Get info about the API - version, allowed query parameters
        self.fetch_api_docs()

        if self.api_version:
            self.headers.update({"Accept": f"application/json; version={self.api_version}"})

        self.fetch_hosts()

        # Interface, and Service lookup will depend on hosts, if option fetch_all is false
        self.refresh_lookups(self.lookup_processes)

        # Looking up IP Addresses depends on the result of interfaces ip_address_count field
        # - can skip any device/vm without any IPs
        self.refresh_lookups(self.lookup_processes_secondary)

        for host in chain(self.devices_list, self.vms_list):
            virtual_chassis_master = self._get_host_virtual_chassis_master(host)
            if virtual_chassis_master is not None and virtual_chassis_master != host["id"]:
                # Device is part of a virtual chassis, but is not the master
                continue

            hostname = self.extract_name(host=host)

            if check_needs_wrapping(hostname):
                hostname = wrap_var(hostname)

            self.inventory.add_host(host=hostname)
            self._fill_host_variables(host=host, hostname=hostname)

            strict = self.get_option("strict")

            # Composed variables
            self._set_composite_vars(self.get_option("compose"), host, hostname, strict=strict)

            # Complex groups based on jinja2 conditionals, hosts that meet the conditional are added to group
            self._add_host_to_composed_groups(self.get_option("groups"), host, hostname, strict=strict)

            # Create groups based on variable values and add the corresponding hosts to it
            self._add_host_to_keyed_groups(self.get_option("keyed_groups"), host, hostname, strict=strict)
            self.add_host_to_groups(host=host, hostname=hostname)

            # Create groups for parent locations, containing child locations
            if "locations" in self.group_by:
                self._add_location_groups()

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path=path)
        self.use_cache = cache

        # Nautobot access
        token = self.get_option("token")
        # Handle extra "/" from api_endpoint configuration and trim if necessary, see PR#49943
        self.api_endpoint = self.get_option("api_endpoint").strip("/")
        self.api_version = self.get_option("api_version")
        self.timeout = self.get_option("timeout")
        self.max_uri_length = self.get_option("max_uri_length")
        self.validate_certs = self.get_option("validate_certs")
        self.follow_redirects = self.get_option("follow_redirects")
        self.config_context = self.get_option("config_context")
        self.flatten_config_context = self.get_option("flatten_config_context")
        self.flatten_local_context_data = self.get_option("flatten_local_context_data")
        self.flatten_custom_fields = self.get_option("flatten_custom_fields")
        self.plurals = self.get_option("plurals")
        self.interfaces = self.get_option("interfaces")
        self.module_interfaces = self.get_option("module_interfaces")
        self.services = self.get_option("services")
        self.fetch_all = self.get_option("fetch_all")
        self.headers = {
            "User-Agent": "ansible %s Python %s" % (ansible_version, python_version.split(" ", maxsplit=1)[0]),
            "Content-type": "application/json",
        }
        if token:
            self.headers.update({"Authorization": "Token %s" % token})

        # Filter and group_by options
        self.group_by = self.get_option("group_by")
        self.group_names_raw = self.get_option("group_names_raw")
        self.query_filters = self.get_option("query_filters")
        self.device_query_filters = self.get_option("device_query_filters")
        self.vm_query_filters = self.get_option("vm_query_filters")
        self.virtual_chassis_name = self.get_option("virtual_chassis_name")
        self.dns_name = self.get_option("dns_name")
        self.ansible_host_dns_name = self.get_option("ansible_host_dns_name")

        # Compile regular expressions, if any
        self.rename_variables = self.parse_rename_variables(self.get_option("rename_variables"))

        self.main()

    def parse_rename_variables(self, rename_variables):
        return [{"pattern": re.compile(i["pattern"]), "repl": i["repl"]} for i in rename_variables or ()]
