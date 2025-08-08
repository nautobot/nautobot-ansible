# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@fragmentedpacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

# Import necessary packages
from ipaddress import ip_interface

from ansible.module_utils._text import to_text
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ENDPOINT_NAME_MAPPING,
    NautobotModule,
)

NB_IP_ADDRESSES = "ip_addresses"
NB_IP_ADDRESS_TO_INTERFACE = "ip_address_to_interface"
NB_NAMESPACES = "namespaces"
NB_PREFIXES = "prefixes"
NB_PREFIX_LOCATIONS = "prefix_location_assignments"
NB_IPAM_ROLES = "roles"
NB_RIRS = "rirs"
NB_ROUTE_TARGETS = "route_targets"
NB_VLANS = "vlans"
NB_VLAN_GROUPS = "vlan_groups"
NB_VLAN_LOCATIONS = "vlan_location_assignments"
NB_VRFS = "vrfs"
NB_VRF_DEVICE_ASSIGNMENTS = "vrf_device_assignments"
NB_SERVICES = "services"


class NautobotIpamModule(NautobotModule):
    def _handle_state_new_present(self, nb_app, nb_endpoint, endpoint_name, name, data):
        if data.get("address"):
            if self.state == "present":
                if self.nb_object and endpoint_name == "ip_address":
                    # namespace is only used for querying in ip_address endpoint, don't pass it to update methods.
                    data.pop("namespace")
                self._ensure_object_exists(nb_endpoint, endpoint_name, name, data)
            elif self.state == "new":
                self.nb_object, diff = self._create_object(nb_endpoint, data)
                self.result["msg"] = "%s %s created" % (endpoint_name, name)
                self.result["changed"] = True
                self.result["diff"] = diff
        else:
            if self.state == "present":
                self._ensure_ip_in_prefix_present_on_netif(nb_app, nb_endpoint, data, endpoint_name)
            elif self.state == "new":
                self._get_new_available_ip_address(nb_app, data, endpoint_name)

    def _ensure_ip_in_prefix_present_on_netif(self, nb_app, nb_endpoint, data, endpoint_name):
        query_params = {
            "parent": data["parent"],
        }

        if data.get("vrf"):
            query_params["vrf_id"] = data["vrf"]

        attached_ips = nb_endpoint.filter(**query_params)
        if attached_ips:
            self.nb_object = attached_ips[-1].serialize()
            self.result["changed"] = False
            self.result["msg"] = "%s %s already attached" % (
                endpoint_name,
                self.nb_object["address"],
            )
        else:
            self._get_new_available_ip_address(nb_app, data, endpoint_name)

    def _get_new_available_ip_address(self, nb_app, data, endpoint_name):
        prefix_query = self._build_query_params("prefix", data)
        prefix = self._nb_endpoint_get(nb_app.prefixes, prefix_query, data["parent"])
        if not prefix:
            self.result["changed"] = False
            self.result["msg"] = "%s does not exist - please create first" % (data["parent"])
        elif prefix.available_ips.list():
            # Convert 'parent' to 'prefix' key when calling prefix endpoint
            data["prefix"] = data.pop("parent")
            self.nb_object, diff = self._create_object(prefix.available_ips, data)
            self.nb_object = self.nb_object.serialize()
            self.result["changed"] = True
            self.result["msg"] = "%s %s created" % (
                endpoint_name,
                self.nb_object["address"],
            )
            self.result["diff"] = diff
        else:
            self.result["changed"] = False
            self.result["msg"] = "No available IPs available within %s" % (data["parent"])

    def _get_new_available_prefix(self, data, endpoint_name):
        if not self.nb_object:
            self.result["changed"] = False
            self.result["msg"] = "Parent prefix does not exist - %s" % (data["parent"])
        elif self.nb_object.available_prefixes.list():
            if self.check_mode:
                self.result["changed"] = True
                self.result["msg"] = "New prefix created within %s" % (data["parent"])
                self.module.exit_json(**self.result)
            # Convert parent to prefix key when calling prefix endpoint
            data["prefix"] = data.pop("parent")
            self.nb_object, diff = self._create_object(self.nb_object.available_prefixes, data)
            self.nb_object = self.nb_object.serialize()
            self.result["changed"] = True
            self.result["msg"] = "%s %s created" % (
                endpoint_name,
                self.nb_object["prefix"],
            )
            self.result["diff"] = diff
        else:
            self.result["changed"] = False
            self.result["msg"] = "No available prefixes within %s" % (data["parent"])

    def run(self):
        """Run the Nautobot IPAM module.

        This function should have all necessary code for endpoints within the application
        to create/update/delete the endpoint objects
        Supported endpoints:
        - ip_addresses
        - ip_address_to_interface
        - prefixes
        - rirs
        - route_targets
        - vlans
        - vlan_groups
        - vrfs
        """
        # Used to dynamically set key when returning results
        endpoint_name = ENDPOINT_NAME_MAPPING[self.endpoint]

        self.result = {"changed": False}

        application = self._find_app(self.endpoint)
        nb_app = getattr(self.nb, application)
        nb_endpoint = getattr(nb_app, self.endpoint)
        user_query_params = self.module.params.get("query_params")

        data = self.data
        if self.endpoint == "ip_addresses":
            if data.get("address"):
                try:
                    data["address"] = to_text(ip_interface(data["address"]).with_prefixlen)
                except ValueError:
                    pass
            name = data.get("address")
        elif self.endpoint in ["prefixes"]:
            name = data.get("prefix")
        elif self.endpoint in [
            "vlan_location_assignments",
            "prefix_location_assignments",
            "vrf_device_assignments",
        ]:
            name = data.get("display")
        else:
            name = data.get("name")

        if self.endpoint in ["vlans", "prefixes"] and self.module.params.get("location"):
            # Need to force the api_version to 2.0 when using `location` parameter
            self.nb.api_version = "2.0"

        if self.module.params.get("first_available"):
            first_available = True
        else:
            first_available = False
        if data.get("parent") and self.endpoint == "ip_addresses":
            object_query_params = self._build_query_params("prefix", data)
            self.nb_object = self._nb_endpoint_get(nb_app.prefixes, object_query_params, name)
        else:
            object_query_params = self._build_query_params(endpoint_name, data, user_query_params)
            self.nb_object = self._nb_endpoint_get(nb_endpoint, object_query_params, name)

        if self.state in ("new", "present") and endpoint_name == "ip_address":
            self._handle_state_new_present(nb_app, nb_endpoint, endpoint_name, name, data)
        elif self.state == "present" and first_available and data.get("parent"):
            self._get_new_available_prefix(data, endpoint_name)
        elif self.state == "present":
            self._ensure_object_exists(nb_endpoint, endpoint_name, name, data)
        elif self.state == "absent":
            self._ensure_object_absent(endpoint_name, name)

        try:
            serialized_object = self.nb_object.serialize()
        except AttributeError:
            serialized_object = self.nb_object

        self.result.update({endpoint_name: serialized_object})

        self.module.exit_json(**self.result)
