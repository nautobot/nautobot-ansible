# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@fragmentedpacket) <mikhail.yohman@gmail.com>
# Copyright: (c) 2018, David Gomez (@amb1s1) <david.gomez@networktocode.com>
# Copyright: (c) 2020, Nokia, Tobias Groß (@toerb) <tobias.gross@nokia.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# Import necessary packages
import traceback
import re
import json
import os

from uuid import UUID
from itertools import chain

from ansible.module_utils.common.text.converters import to_text

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.urls import open_url

PYNAUTOBOT_IMP_ERR = None
try:
    import pynautobot

    HAS_PYNAUTOBOT = True
except ImportError:
    PYNAUTOBOT_IMP_ERR = traceback.format_exc()
    HAS_PYNAUTOBOT = False

# Used to map endpoints to applications dynamically
API_APPS_ENDPOINTS = dict(
    circuits=["circuits", "circuit_types", "circuit_terminations", "providers"],
    dcim=[
        "cables",
        "console_ports",
        "console_port_templates",
        "console_server_ports",
        "console_server_port_templates",
        "device_bays",
        "device_bay_templates",
        "devices",
        "device_roles",
        "device_types",
        "front_ports",
        "front_port_templates",
        "interfaces",
        "interface_templates",
        "inventory_items",
        "manufacturers",
        "platforms",
        "power_feeds",
        "power_outlets",
        "power_outlet_templates",
        "power_panels",
        "power_ports",
        "power_port_templates",
        "racks",
        "rack_groups",
        "rack_roles",
        "rear_ports",
        "rear_port_templates",
        "regions",
        "sites",
        "virtual_chassis",
    ],
    extras=["tags", "statuses"],
    ipam=[
        "aggregates",
        "ip_addresses",
        "prefixes",
        "rirs",
        "roles",
        "route_targets",
        "vlans",
        "vlan_groups",
        "vrfs",
        "services",
    ],
    secrets=[],
    tenancy=["tenants", "tenant_groups"],
    virtualization=["cluster_groups", "cluster_types", "clusters", "virtual_machines"],
)

# Used to normalize data for the respective query types used to find endpoints
QUERY_TYPES = dict(
    circuit="cid",
    circuit_termination="circuit",
    circuit_type="slug",
    cluster="name",
    cluster_group="slug",
    cluster_type="slug",
    device="name",
    device_role="slug",
    device_type="slug",
    export_targets="name",
    group="slug",
    installed_device="name",
    import_targets="name",
    manufacturer="slug",
    nat_inside="address",
    nat_outside="address",
    parent_rack_group="slug",
    parent_region="slug",
    power_panel="name",
    power_port="name",
    power_port_template="name",
    platform="slug",
    prefix_role="slug",
    primary_ip="address",
    primary_ip4="address",
    primary_ip6="address",
    provider="slug",
    rack="name",
    rack_group="slug",
    rack_role="slug",
    rear_port="name",
    rear_port_template="name",
    region="slug",
    rir="slug",
    route_targets="name",
    slug="slug",
    site="slug",
    tenant="slug",
    tenant_group="slug",
    time_zone="timezone",
    virtual_chassis="name",
    virtual_machine="name",
    virtual_machine_role="slug",
    vlan="name",
    vlan_group="slug",
    vlan_role="name",
    vrf="name",
)

# Specifies keys within data that need to be converted to ID and the endpoint to be used when queried
CONVERT_TO_ID = {
    "assigned_object": "assigned_object",
    "circuit": "circuits",
    "circuit_type": "circuit_types",
    "circuit_termination": "circuit_terminations",
    "circuits.circuittermination": "circuit_terminations",
    "cluster": "clusters",
    "cluster_group": "cluster_groups",
    "cluster_type": "cluster_types",
    "dcim.consoleport": "console_ports",
    "dcim.consoleserverport": "console_server_ports",
    "dcim.frontport": "front_ports",
    "dcim.interface": "interfaces",
    "dcim.powerfeed": "power_feeds",
    "dcim.poweroutlet": "power_outlets",
    "dcim.powerport": "power_ports",
    "dcim.rearport": "rear_ports",
    "device": "devices",
    "device_role": "device_roles",
    "device_type": "device_types",
    "export_targets": "route_targets",
    "group": "tenant_groups",
    "import_targets": "route_targets",
    "installed_device": "devices",
    "interface": "interfaces",
    "interface_template": "interface_templates",
    "ip_addresses": "ip_addresses",
    "ipaddresses": "ip_addresses",
    "lag": "interfaces",
    "manufacturer": "manufacturers",
    "master": "devices",
    "nat_inside": "ip_addresses",
    "nat_outside": "ip_addresses",
    "platform": "platforms",
    "parent_rack_group": "rack_groups",
    "parent_region": "regions",
    "power_panel": "power_panels",
    "power_port": "power_ports",
    "power_port_template": "power_port_templates",
    "prefix_role": "roles",
    "primary_ip": "ip_addresses",
    "primary_ip4": "ip_addresses",
    "primary_ip6": "ip_addresses",
    "provider": "providers",
    "rack": "racks",
    "rack_group": "rack_groups",
    "rack_role": "rack_roles",
    "region": "regions",
    "rear_port": "rear_ports",
    "rear_port_template": "rear_port_templates",
    "rir": "rirs",
    "route_targets": "route_targets",
    "services": "services",
    "site": "sites",
    "tags": "tags",
    "tagged_vlans": "vlans",
    "tenant": "tenants",
    "tenant_group": "tenant_groups",
    "termination_a": "interfaces",
    "termination_b": "interfaces",
    "untagged_vlan": "vlans",
    "virtual_chassis": "virtual_chassis",
    "virtual_machine": "virtual_machines",
    "virtual_machine_role": "device_roles",
    "vlan": "vlans",
    "vlan_group": "vlan_groups",
    "vlan_role": "roles",
    "vrf": "vrfs",
}

ENDPOINT_NAME_MAPPING = {
    "aggregates": "aggregate",
    "cables": "cable",
    "circuit_terminations": "circuit_termination",
    "circuit_types": "circuit_type",
    "circuits": "circuit",
    "clusters": "cluster",
    "cluster_groups": "cluster_group",
    "cluster_types": "cluster_type",
    "console_ports": "console_port",
    "console_port_templates": "console_port_template",
    "console_server_ports": "console_server_port",
    "console_server_port_templates": "console_server_port_template",
    "device_bays": "device_bay",
    "device_bay_templates": "device_bay_template",
    "devices": "device",
    "device_roles": "device_role",
    "device_types": "device_type",
    "front_ports": "front_port",
    "front_port_templates": "front_port_template",
    "interfaces": "interface",
    "interface_templates": "interface_template",
    "inventory_items": "inventory_item",
    "ip_addresses": "ip_address",
    "manufacturers": "manufacturer",
    "platforms": "platform",
    "power_feeds": "power_feed",
    "power_outlets": "power_outlet",
    "power_outlet_templates": "power_outlet_template",
    "power_panels": "power_panel",
    "power_ports": "power_port",
    "power_port_templates": "power_port_template",
    "prefixes": "prefix",
    "providers": "provider",
    "racks": "rack",
    "rack_groups": "rack_group",
    "rack_roles": "rack_role",
    "rear_ports": "rear_port",
    "rear_port_templates": "rear_port_template",
    "regions": "region",
    "rirs": "rir",
    "roles": "role",
    "route_targets": "route_target",
    "services": "services",
    "sites": "site",
    "statuses": "statuses",
    "tags": "tags",
    "tenants": "tenant",
    "tenant_groups": "tenant_group",
    "virtual_chassis": "virtual_chassis",
    "virtual_machines": "virtual_machine",
    "vlans": "vlan",
    "vlan_groups": "vlan_group",
    "vrfs": "vrf",
}

# What makes the search unique
ALLOWED_QUERY_PARAMS = {
    "aggregate": set(["prefix", "rir"]),
    "assigned_object": set(["name", "device", "virtual_machine"]),
    "circuit": set(["cid"]),
    "circuit_type": set(["slug"]),
    "circuit_termination": set(["circuit", "term_side"]),
    "circuits.circuittermination": set(["circuit", "term_side"]),
    "cluster": set(["name", "type"]),
    "cluster_group": set(["slug"]),
    "cluster_type": set(["slug"]),
    "console_port": set(["name", "device"]),
    "console_port_template": set(["name", "device_type"]),
    "console_server_port": set(["name", "device"]),
    "console_server_port_template": set(["name", "device_type"]),
    "dcim.consoleport": set(["name", "device"]),
    "dcim.consoleserverport": set(["name", "device"]),
    "dcim.frontport": set(["name", "device", "rear_port"]),
    "dcim.interface": set(["name", "device", "virtual_machine"]),
    "dcim.powerfeed": set(["name", "power_panel"]),
    "dcim.poweroutlet": set(["name", "device"]),
    "dcim.powerport": set(["name", "device"]),
    "dcim.rearport": set(["name", "device"]),
    "device_bay": set(["name", "device"]),
    "device_bay_template": set(["name", "device_type"]),
    "device": set(["name"]),
    "device_role": set(["slug"]),
    "device_type": set(["slug"]),
    "front_port": set(["name", "device", "rear_port"]),
    "front_port_template": set(["name", "device_type", "rear_port"]),
    "installed_device": set(["name"]),
    "interface": set(["name", "device", "virtual_machine"]),
    "interface_template": set(["name", "device_type"]),
    "inventory_item": set(["name", "device"]),
    "ip_address": set(["address", "vrf", "device", "interface", "assigned_object"]),
    "ip_addresses": set(["address", "vrf", "device", "interface", "assigned_object"]),
    "ipaddresses": set(["address", "vrf", "device", "interface", "assigned_object"]),
    "lag": set(["name"]),
    "manufacturer": set(["slug"]),
    "master": set(["name"]),
    "nat_inside": set(["vrf", "address"]),
    "parent_rack_group": set(["slug"]),
    "parent_region": set(["slug"]),
    "platform": set(["slug"]),
    "power_feed": set(["name", "power_panel"]),
    "power_outlet": set(["name", "device"]),
    "power_outlet_template": set(["name", "device_type"]),
    "power_panel": set(["name", "site"]),
    "power_port": set(["name", "device"]),
    "power_port_template": set(["name", "device_type"]),
    "prefix": set(["prefix", "vrf"]),
    "primary_ip4": set(["address", "vrf"]),
    "primary_ip6": set(["address", "vrf"]),
    "provider": set(["slug"]),
    "rack": set(["name", "site"]),
    "rack_group": set(["slug"]),
    "rack_role": set(["slug"]),
    "region": set(["slug"]),
    "rear_port": set(["name", "device"]),
    "rear_port_template": set(["name", "device_type"]),
    "rir": set(["slug"]),
    "role": set(["slug"]),
    "route_target": set(["name"]),
    "services": set(["device", "virtual_machine", "name", "port", "protocol"]),
    "site": set(["slug"]),
    "statuses": set(["name"]),
    "tags": set(["slug"]),
    "tagged_vlans": set(["group", "name", "site", "vid", "vlan_group", "tenant"]),
    "tenant": set(["slug"]),
    "tenant_group": set(["slug"]),
    "termination_a": set(["name", "device", "virtual_machine"]),
    "termination_b": set(["name", "device", "virtual_machine"]),
    "untagged_vlan": set(["group", "name", "site", "vid", "vlan_group", "tenant"]),
    "virtual_chassis": set(["name", "device"]),
    "virtual_machine": set(["name", "cluster"]),
    "vlan": set(["group", "name", "site", "tenant", "vid", "vlan_group"]),
    "vlan_group": set(["slug", "site"]),
    "vrf": set(["name", "tenant"]),
}

QUERY_PARAMS_IDS = set(
    [
        "circuit",
        "cluster",
        "device",
        "group",
        "interface",
        "rir",
        "vrf",
        "site",
        "tenant",
        "type",
        "virtual_machine",
    ]
)

REQUIRED_ID_FIND = {
    "cables": set(["status", "type", "length_unit"]),
    "circuits": set(["status"]),
    "console_ports": set(["type"]),
    "console_port_templates": set(["type"]),
    "console_server_ports": set(["type"]),
    "console_server_port_templates": set(["type"]),
    "devices": set(["status", "face"]),
    "device_types": set(["subdevice_role"]),
    "front_ports": set(["type"]),
    "front_port_templates": set(["type"]),
    "interfaces": set(["form_factor", "mode", "type"]),
    "interface_templates": set(["type"]),
    "ip_addresses": set(["status", "role"]),
    "prefixes": set(["status"]),
    "power_feeds": set(["status", "type", "supply", "phase"]),
    "power_outlets": set(["type", "feed_leg"]),
    "power_outlet_templates": set(["type", "feed_leg"]),
    "power_ports": set(["type"]),
    "power_port_templates": set(["type"]),
    "racks": set(["status", "outer_unit", "type"]),
    "rear_ports": set(["type"]),
    "rear_port_templates": set(["type"]),
    "services": set(["protocol"]),
    "sites": set(["status"]),
    "virtual_machines": set(["status", "face"]),
    "vlans": set(["status"]),
}

# This is used to map non-clashing keys to Nautobot API compliant keys to prevent bad logic in code for similar keys but different modules
CONVERT_KEYS = {
    "assigned_object": "assigned_object_id",
    "circuit_type": "type",
    "cluster_type": "type",
    "cluster_group": "group",
    "parent_rack_group": "parent",
    "parent_region": "parent",
    "power_port_template": "power_port",
    "prefix_role": "role",
    "rack_group": "group",
    "rack_role": "role",
    "rear_port_template": "rear_port",
    "rear_port_template_position": "rear_port_position",
    "tenant_group": "group",
    "termination_a": "termination_a_id",
    "termination_b": "termination_b_id",
    "virtual_machine_role": "role",
    "vlan_role": "role",
    "vlan_group": "group",
}

# This is used to dynamically convert name to slug on endpoints requiring a slug
SLUG_REQUIRED = {
    "circuit_types",
    "cluster_groups",
    "cluster_types",
    "device_roles",
    "device_types",
    "ipam_roles",
    "rack_groups",
    "rack_roles",
    "regions",
    "rirs",
    "roles",
    "sites",
    "statuses",
    "tags",
    "tenants",
    "tenant_groups",
    "manufacturers",
    "platforms",
    "providers",
    "vlan_groups",
}

NAUTOBOT_ARG_SPEC = dict(
    url=dict(type="str", required=True),
    token=dict(type="str", required=True, no_log=True),
    state=dict(required=False, default="present", choices=["present", "absent"]),
    query_params=dict(required=False, type="list", elements="str"),
    validate_certs=dict(type="raw", default=True),
)


class NautobotModule:
    """
    Initialize connection to Nautobot, sets AnsibleModule passed in to
    self.module to be used throughout the class
    :params module (obj): Ansible Module object
    :params endpoint (str): Used to tell class which endpoint the logic needs to follow
    :params nb_client (obj): pynautobot.api object passed in (not required)
    """

    def __init__(self, module, endpoint, client=None, remove_keys=None):
        self.module = module
        self.state = self.module.params["state"]
        self.check_mode = self.module.check_mode
        self.endpoint = endpoint
        query_params = self.module.params.get("query_params")

        if not HAS_PYNAUTOBOT:
            self.module.fail_json(
                msg=missing_required_lib("pynautobot"), exception=PYNAUTOBOT_IMP_ERR
            )
        # These should not be required after making connection to Nautobot
        url = self.module.params["url"]
        token = self.module.params["token"]
        ssl_verify = self.module.params["validate_certs"]

        # Attempt to initiate connection to Nautobot
        if client is None:
            self.nb = self._connect_api(url, token, ssl_verify)
        else:
            self.nb = client
            self.version = self.nb.version

        # if self.module.params.get("query_params"):
        #    self._validate_query_params(self.module.params["query_params"])

        # These methods will normalize the regular data
        cleaned_data = self._remove_arg_spec_default(module.params)
        norm_data = self._normalize_data(cleaned_data)
        choices_data = self._change_choices_id(self.endpoint, norm_data)
        data = self._find_ids(choices_data, query_params)
        data = self._convert_identical_keys(data)
        self.data = self._build_payload(data, remove_keys)

    def _build_payload(self, data, remove_keys):
        """Remove any key/value pairs that aren't relevant for interacting with Nautobot.

        Args:
            data ([type]): [description]
            remove_keys ([type]): [description]

        Returns:
            [type]: [description]
        """
        keys_to_remove = set(NAUTOBOT_ARG_SPEC)
        if remove_keys:
            keys_to_remove.update(remove_keys)

        return {k: v for k, v in data.items() if k not in keys_to_remove}

    def _version_check_greater(self, greater, lesser, greater_or_equal=False):
        """Determine if first argument is greater than second argument.

        Args:
            greater (str): decimal string
            lesser (str): decimal string
        """
        g_major, g_minor = greater.split(".")
        l_major, l_minor = lesser.split(".")

        # convert to ints
        g_major = int(g_major)
        g_minor = int(g_minor)
        l_major = int(l_major)
        l_minor = int(l_minor)

        # If major version is higher then return true right off the bat
        if g_major > l_major:
            return True
        elif greater_or_equal and g_major == l_major and g_minor >= l_minor:
            return True
        # If major versions are equal, and minor version is higher, return True
        elif g_major == l_major and g_minor > l_minor:
            return True

    def _connect_api(self, url, token, ssl_verify):
        try:
            nb = pynautobot.api(url, token=token)
            nb.http_session.verify = ssl_verify
            try:
                self.version = nb.version
            except Exception:
                self.module.fail_json(
                    msg="Failed to establish connection to Nautobot API"
                )
            return nb
        except Exception:
            self.module.fail_json(msg="Failed to establish connection to Nautobot API")

    def _nb_endpoint_get(self, nb_endpoint, query_params, search_item):
        try:
            response = nb_endpoint.get(**query_params)
        except pynautobot.RequestError as e:
            self._handle_errors(msg=e.error)
        except ValueError:
            self._handle_errors(
                msg="More than one result returned for %s" % (search_item)
            )

        return response

    def _validate_query_params(self, query_params):
        """
        Validate query_params that are passed in by users to make sure
        they're valid and return error if they're not valid.
        """
        invalid_query_params = []

        app = self._find_app(self.endpoint)
        nb_app = getattr(self.nb, app)
        nb_endpoint = getattr(nb_app, self.endpoint)
        # Fetch the OpenAPI spec to perform validation against
        base_url = self.nb.base_url
        junk, endpoint_url = nb_endpoint.url.split(base_url)
        response = open_url(base_url + "/docs/?format=openapi")
        try:
            raw_data = to_text(response.read(), errors="surrogate_or_strict")
        except UnicodeError:
            self._handle_errors(
                msg="Incorrect encoding of fetched payload from Nautobot API."
            )

        try:
            openapi = json.loads(raw_data)
        except ValueError:
            self._handle_errors(msg="Incorrect JSON payload returned: %s" % raw_data)

        valid_query_params = openapi["paths"][endpoint_url + "/"]["get"]["parameters"]

        # Loop over passed in params and add to invalid_query_params and then fail if non-empty
        for param in query_params:
            if param not in valid_query_params:
                invalid_query_params.append(param)

        if invalid_query_params:
            self._handle_errors(
                "The following query_params are invalid: {0}".format(
                    ", ".join(invalid_query_params)
                )
            )

    def _handle_errors(self, msg):
        """
        Returns message and changed = False
        :params msg (str): Message indicating why there is no change
        """
        self.module.fail_json(msg=msg, changed=False)

    def _build_diff(self, before=None, after=None):
        """Builds diff of before and after changes"""
        return {"before": before, "after": after}

    def _convert_identical_keys(self, data):
        """
        Used to change non-clashing keys for each module into identical keys that are required
        to be passed to pynautobot
        ex. rack_role back into role to pass to Nautobot
        Returns data
        :params data (dict): Data dictionary after _find_ids method ran
        """
        temp_dict = dict()
        for key in data:
            if self.endpoint == "power_panels" and key == "rack_group":
                temp_dict[key] = data[key]
            elif key in CONVERT_KEYS:
                # This will keep the original key for assigned_object, but also convert to assigned_object_id
                if key == "assigned_object":
                    temp_dict[key] = data[key]
                new_key = CONVERT_KEYS[key]
                temp_dict[new_key] = data[key]
            else:
                temp_dict[key] = data[key]

        return temp_dict

    def _remove_arg_spec_default(self, data):
        """Used to remove any data keys that were not provided by user, but has the arg spec
        default values
        """
        new_dict = dict()
        for k, v in data.items():
            if isinstance(v, dict):
                v = self._remove_arg_spec_default(v)
                new_dict[k] = v
            elif v is not None:
                new_dict[k] = v

        return new_dict

    def is_valid_uuid(self, match):
        """Determine if the match is already UUID."""
        try:
            uuid_obj = UUID(match)
        except (ValueError, AttributeError):
            return False
        return str(uuid_obj) == match

    def _get_query_param_id(self, match, data):
        """Used to find IDs of necessary searches when required under _build_query_params
        :returns id (int) or data (dict): Either returns the ID or original data passed in
        :params match (str): The key within the user defined data that is required to have an ID
        :params data (dict): User defined data passed into the module
        """

        match_value = data.get(match)
        if isinstance(match_value, int) or self.is_valid_uuid(match_value):
            return match_value

        endpoint = CONVERT_TO_ID[match]
        app = self._find_app(endpoint)
        nb_app = getattr(self.nb, app)
        nb_endpoint = getattr(nb_app, endpoint)

        query_params = {QUERY_TYPES.get(match): data[match]}
        result = self._nb_endpoint_get(nb_endpoint, query_params, match)

        if result:
            return result.id
        else:
            return data

    def _build_query_params(
        self, parent, module_data, user_query_params=None, child=None
    ):
        """
        :returns dict(query_dict): Returns a query dictionary built using mappings to dynamically
        build available query params for Nautobot endpoints
        :params parent(str): This is either a key from `_find_ids` or a string passed in to determine
        which keys in the data that we need to use to construct `query_dict`
        :params module_data(dict): Uses the data provided to the Nautobot module
        :params child(dict): This is used within `_find_ids` and passes the inner dictionary
        to build the appropriate `query_dict` for the parent
        """
        # This is to change the parent key to use the proper ALLOWED_QUERY_PARAMS below for termination searches.
        if parent == "termination_a" and module_data.get("termination_a_type"):
            parent = module_data["termination_a_type"]
        elif parent == "termination_b" and module_data.get("termination_b_type"):
            parent = module_data["termination_b_type"]

        query_dict = dict()
        if user_query_params:
            query_params = set(user_query_params)
        else:
            query_params = ALLOWED_QUERY_PARAMS.get(parent)

        if child:
            matches = query_params.intersection(set(child.keys()))
        else:
            matches = query_params.intersection(set(module_data.keys()))

        for match in matches:
            if match in QUERY_PARAMS_IDS:
                if child:
                    query_id = self._get_query_param_id(match, child)
                else:
                    query_id = self._get_query_param_id(match, module_data)
                query_dict.update({match + "_id": query_id})
            else:
                if child:
                    value = child.get(match)
                else:
                    value = module_data.get(match)
                query_dict.update({match: value})

        if user_query_params:
            # This is to skip any potential changes using module_data when the user
            # provides user_query_params
            pass
        elif parent == "lag":
            if not child:
                query_dict["name"] = module_data["lag"]
            intf_type = self._fetch_choice_value(
                "Link Aggregation Group (LAG)", "interfaces"
            )
            query_dict.update({"type": intf_type})
            if isinstance(module_data["device"], int) or self.is_valid_uuid(
                module_data["device"]
            ):
                query_dict.update({"device_id": module_data["device"]})
            else:
                query_dict.update({"device": module_data["device"]})

        elif parent == "prefix" and module_data.get("parent"):
            query_dict.update({"prefix": module_data["parent"]})

        elif parent == "ip_addresses":
            if isinstance(module_data["device"], int) or self.is_valid_uuid(
                module_data["device"]
            ):
                query_dict.update({"device_id": module_data["device"]})
            else:
                query_dict.update({"device": module_data["device"]})

        elif (
            parent == "ip_address"
            and "assigned_object" in matches
            and module_data.get("assigned_object_type")
        ):
            if module_data["assigned_object_type"] == "virtualization.vminterface":
                query_dict.update(
                    {"vminterface_id": module_data.get("assigned_object_id")}
                )
            elif module_data["assigned_object_type"] == "dcim.interface":
                query_dict.update(
                    {"interface_id": module_data.get("assigned_object_id")}
                )

        elif parent == "rear_port" and self.endpoint == "front_ports":
            if isinstance(module_data.get("rear_port"), str):
                rear_port = {
                    "device_id": module_data.get("device"),
                    "name": module_data.get("rear_port"),
                }
                query_dict.update(rear_port)

        elif parent == "rear_port_template" and self.endpoint == "front_port_templates":
            if isinstance(module_data.get("rear_port_template"), str):
                rear_port_template = {
                    "devicetype_id": module_data.get("device_type"),
                    "name": module_data.get("rear_port_template"),
                }
                query_dict.update(rear_port_template)

        elif "_template" in parent:
            if query_dict.get("device_type"):
                query_dict["devicetype_id"] = query_dict.pop("device_type")

        if not query_dict:
            provided_kwargs = child.keys() if child else module_data.keys()
            acceptable_query_params = (
                user_query_params if user_query_params else query_params
            )
            self._handle_errors(
                f"One or more of the kwargs provided are invalid for {parent}, provided kwargs: {', '.join(sorted(provided_kwargs))}. Acceptable kwargs: {', '.join(sorted(acceptable_query_params))}"
            )

        query_dict = self._convert_identical_keys(query_dict)
        return query_dict

    def _fetch_choice_value(self, search, endpoint):
        app = self._find_app(endpoint)
        nb_app = getattr(self.nb, app)
        nb_endpoint = getattr(nb_app, endpoint)
        try:
            endpoint_choices = nb_endpoint.choices()
        except ValueError:
            self._handle_errors(
                msg="Failed to fetch endpoint choices to validate against. This requires a write-enabled token. Make sure the token is write-enabled. If looking to fetch only information, use either the inventory or lookup plugin."
            )

        choices = [x for x in chain.from_iterable(endpoint_choices.values())]

        for item in choices:
            if item["display"].lower() == search.lower():
                return item["value"]
            elif item["value"] == search.lower():
                return item["value"]
        self._handle_errors(
            msg="%s was not found as a valid choice for %s" % (search, endpoint)
        )

    def _change_choices_id(self, endpoint, data):
        """Used to change data that is static and under _choices for the application.
        ex. DEVICE_STATUS
        :returns data (dict): Returns the user defined data back with updated fields for _choices
        :params endpoint (str): The endpoint that will be used for mapping to required _choices
        :params data (dict): User defined data passed into the module
        """
        if REQUIRED_ID_FIND.get(endpoint):
            required_choices = REQUIRED_ID_FIND[endpoint]
            for choice in required_choices:
                if data.get(choice):
                    if isinstance(data[choice], int) or self.is_valid_uuid(
                        data[choice]
                    ):
                        continue
                    choice_value = self._fetch_choice_value(data[choice], endpoint)
                    data[choice] = choice_value

        return data

    def _find_app(self, endpoint):
        """Dynamically finds application of endpoint passed in using the
        API_APPS_ENDPOINTS for mapping
        :returns nb_app (str): The application the endpoint lives under
        :params endpoint (str): The endpoint requiring resolution to application
        """
        for k, v in API_APPS_ENDPOINTS.items():
            if endpoint in v:
                nb_app = k
        return nb_app

    def _find_ids(self, data, user_query_params):
        """Will find the IDs of all user specified data if resolvable
        :returns data (dict): Returns the updated dict with the IDs of user specified data
        :params data (dict): User defined data passed into the module
        """
        for k, v in data.items():
            if k in CONVERT_TO_ID:
                if k == "termination_a":
                    endpoint = CONVERT_TO_ID[data.get("termination_a_type")]
                elif k == "termination_b":
                    endpoint = CONVERT_TO_ID[data.get("termination_b_type")]
                elif k == "assigned_object":
                    endpoint = "interfaces"
                else:
                    endpoint = CONVERT_TO_ID[k]
                search = v
                app = self._find_app(endpoint)
                nb_app = getattr(self.nb, app)
                nb_endpoint = getattr(nb_app, endpoint)

                if isinstance(v, dict):
                    if (k == "interface" or k == "assigned_object") and v.get(
                        "virtual_machine"
                    ):
                        nb_app = getattr(self.nb, "virtualization")
                        nb_endpoint = getattr(nb_app, endpoint)
                    query_params = self._build_query_params(k, data, child=v)
                    query_id = self._nb_endpoint_get(nb_endpoint, query_params, k)
                elif isinstance(v, list):
                    id_list = list()
                    for list_item in v:
                        if (
                            k == "tags"
                            and isinstance(list_item, str)
                            and not self.is_valid_uuid(list_item)
                        ):
                            temp_dict = {"slug": self._to_slug(list_item)}
                        elif isinstance(list_item, dict):
                            norm_data = self._normalize_data(list_item)
                            temp_dict = self._build_query_params(
                                k, data, child=norm_data
                            )
                        # If user passes in an integer, add to ID list to id_list as user
                        # should have passed in a tag ID
                        elif isinstance(list_item, int) or self.is_valid_uuid(
                            list_item
                        ):
                            id_list.append(list_item)
                            continue
                        else:
                            temp_dict = {QUERY_TYPES.get(k, "q"): search}

                        query_id = self._nb_endpoint_get(nb_endpoint, temp_dict, k)
                        if query_id:
                            id_list.append(query_id.id)
                        else:
                            self._handle_errors(msg="%s not found" % (list_item))
                else:
                    if k in ["lag", "rear_port", "rear_port_template"]:
                        query_params = self._build_query_params(
                            k, data, user_query_params
                        )
                    else:
                        query_params = {QUERY_TYPES.get(k, "q"): search}
                    query_id = self._nb_endpoint_get(nb_endpoint, query_params, k)

                if isinstance(v, list):
                    data[k] = id_list
                elif isinstance(v, int) or self.is_valid_uuid(v):
                    pass
                elif query_id:
                    data[k] = query_id.id
                else:
                    self._handle_errors(msg="Could not resolve id of %s: %s" % (k, v))

        return data

    def _to_slug(self, value):
        """
        :returns slug (str): Slugified value
        :params value (str): Value that needs to be changed to slug format
        """
        if value is None:
            return value
        elif isinstance(value, int) or self.is_valid_uuid(value):
            return value
        else:
            removed_chars = re.sub(r"[^\-\.\w\s]", "", value)
            convert_chars = re.sub(r"[\-\.\s]+", "-", removed_chars)
            return convert_chars.strip().lower()

    def _normalize_data(self, data):
        """
        :returns data (dict): Normalized module data to formats accepted by Nautobot searches
        such as changing from user specified value to slug
        ex. Test Rack -> test-rack
        :params data (dict): Original data from Nautobot module
        """
        for k, v in data.items():
            if isinstance(v, dict):
                if v.get("id"):
                    if self.is_valid_uuid(v["id"]):
                        data[k] = v["id"]
                        continue
                    else:
                        self._handle_errors(f"Invalid ID passed for {k}: {v['id']}")

                for subk, subv in v.items():
                    sub_data_type = QUERY_TYPES.get(subk, "q")
                    if sub_data_type == "slug":
                        data[k][subk] = self._to_slug(subv)
            else:
                data_type = QUERY_TYPES.get(k, "q")
                if data_type == "slug":
                    data[k] = self._to_slug(v)
                elif data_type == "timezone":
                    if " " in v:
                        data[k] = v.replace(" ", "_")
            if k == "description":
                data[k] = v.strip()

            if k == "mac_address":
                data[k] = v.upper()

        # We need to assign the correct type for the assigned object so the user doesn't have to worry about this.
        # We determine it by whether or not they pass in a device or virtual_machine
        if data.get("assigned_object"):
            if data["assigned_object"].get("device"):
                data["assigned_object_type"] = "dcim.interface"
            if data["assigned_object"].get("virtual_machine"):
                data["assigned_object_type"] = "virtualization.vminterface"

        return data

    def _create_object(self, nb_endpoint, data):
        """Create a Nautobot object.
        :returns tuple(serialized_nb_obj, diff): tuple of the serialized created
        Nautobot object and the Ansible diff.
        """
        if self.check_mode:
            nb_obj = data
        else:
            try:
                nb_obj = nb_endpoint.create(data)
            except pynautobot.RequestError as e:
                self._handle_errors(msg=e.error)

        diff = self._build_diff(before={"state": "absent"}, after={"state": "present"})
        return nb_obj, diff

    def _delete_object(self):
        """Delete a Nautobot object.
        :returns diff (dict): Ansible diff
        """
        if not self.check_mode:
            try:
                self.nb_object.delete()
            except pynautobot.RequestError as e:
                self._handle_errors(msg=e.error)

        diff = self._build_diff(before={"state": "present"}, after={"state": "absent"})
        return diff

    def _update_object(self, data):
        """Update a Nautobot object.
        :returns tuple(serialized_nb_obj, diff): tuple of the serialized updated
        Nautobot object and the Ansible diff.
        """
        serialized_nb_obj = self.nb_object.serialize()
        updated_obj = serialized_nb_obj.copy()
        updated_obj.update(data)
        if serialized_nb_obj.get("tags") and data.get("tags"):
            serialized_nb_obj["tags"] = set(serialized_nb_obj["tags"])
            updated_obj["tags"] = set(data["tags"])

        if serialized_nb_obj == updated_obj:
            return serialized_nb_obj, None
        else:
            data_before, data_after = {}, {}
            for key in data:
                try:
                    if serialized_nb_obj[key] != updated_obj[key]:
                        data_before[key] = serialized_nb_obj[key]
                        data_after[key] = updated_obj[key]
                except KeyError:
                    if key == "form_factor":
                        msg = "form_factor is not valid for Nautobot 2.7 onword. Please use the type key instead."
                    else:
                        msg = (
                            "%s does not exist on existing object. Check to make sure valid field."
                            % (key)
                        )

                    self._handle_errors(msg=msg)

            if not self.check_mode:
                self.nb_object.update(data)
                updated_obj = self.nb_object.serialize()

            diff = self._build_diff(before=data_before, after=data_after)
            return updated_obj, diff

    def _ensure_object_exists(self, nb_endpoint, endpoint_name, name, data):
        """Used when `state` is present to make sure object exists or if the object exists
        that it is updated
        :params nb_endpoint (pynautobot endpoint object): This is the nb endpoint to be used
        to create or update the object
        :params endpoint_name (str): Endpoint name that was created/updated. ex. device
        :params name (str): Name of the object
        :params data (dict): User defined data passed into the module
        """
        if not self.nb_object:
            self.nb_object, diff = self._create_object(nb_endpoint, data)
            self.result["msg"] = "%s %s created" % (endpoint_name, name)
            self.result["changed"] = True
            self.result["diff"] = diff
        else:
            self.nb_object, diff = self._update_object(data)
            if self.nb_object is False:
                self._handle_errors(
                    msg="Request failed, couldn't update device: %s" % name
                )
            if diff:
                self.result["msg"] = "%s %s updated" % (endpoint_name, name)
                self.result["changed"] = True
                self.result["diff"] = diff
            else:
                self.result["msg"] = "%s %s already exists" % (endpoint_name, name)

    def _ensure_object_absent(self, endpoint_name, name):
        """Used when `state` is absent to make sure object does not exist
        :params endpoint_name (str): Endpoint name that was created/updated. ex. device
        :params name (str): Name of the object
        """
        if self.nb_object:
            diff = self._delete_object()
            self.result["msg"] = "%s %s deleted" % (endpoint_name, name)
            self.result["changed"] = True
            self.result["diff"] = diff
        else:
            self.result["msg"] = "%s %s already absent" % (endpoint_name, name)

    def run(self):
        """
        Must be implemented in subclasses
        """
        raise NotImplementedError


class NautobotApiBase:
    def __init__(self, **kwargs):
        self.url = kwargs.get("url") or os.getenv("NAUTOBOT_URL")
        self.token = kwargs.get("token") or os.getenv("NAUTOBOT_TOKEN")
        self.ssl_verify = kwargs.get("ssl_verify", True)

        # Setup the API client calls
        self.api = pynautobot.api(url=self.url, token=self.token)
        self.api.http_session.verify = self.ssl_verify


class NautobotGraphQL:
    def __init__(self, query_str, api=None, variables=None):
        self.query_str = query_str
        self.pynautobot = api.api
        self.variables = variables

    def query(self):
        """Makes API call and checks response from GraphQL endpoint."""
        # Make API call to query
        graph_response = self.pynautobot.graphql.query(
            query=self.query_str, variables=self.variables
        )

        return graph_response
