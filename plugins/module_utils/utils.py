# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@fragmentedpacket) <mikhail.yohman@gmail.com>
# Copyright: (c) 2018, David Gomez (@amb1s1) <david.gomez@networktocode.com>
# Copyright: (c) 2020, Nokia, Tobias Groß (@toerb) <tobias.gross@nokia.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# Import necessary packages
import json
import os
import traceback
from itertools import chain
from uuid import UUID

from ansible.module_utils.basic import env_fallback, missing_required_lib
from ansible.module_utils.common.text.converters import to_text
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
    cloud=[
        "cloud_accounts",
        "cloud_networks",
        "cloud_network_prefix_assignments",
        "cloud_resource_types",
        "cloud_services",
        "cloud_service_network_assignments",
    ],
    dcim=[
        "cables",
        "console_ports",
        "console_port_templates",
        "console_server_ports",
        "console_server_port_templates",
        "controllers",
        "controller_managed_device_groups",
        "device_bays",
        "device_bay_templates",
        "device_cluster_assignments",
        "devices",
        "device_families",
        "device_types",
        "device_redundancy_groups",
        "front_ports",
        "front_port_templates",
        "interfaces",
        "interface_templates",
        "inventory_items",
        "locations",
        "location_types",
        "manufacturers",
        "module_bay_templates",
        "module_bays",
        "module_types",
        "modules",
        "platforms",
        "power_feeds",
        "power_outlets",
        "power_outlet_templates",
        "power_panels",
        "power_ports",
        "power_port_templates",
        "racks",
        "rack_groups",
        "rear_ports",
        "rear_port_templates",
        "software_versions",
        "software_image_files",
        "virtual_chassis",
    ],
    extras=[
        "contacts",
        "custom_fields",
        "custom_field_choices",
        "metadata_choices",
        "metadata_types",
        "object_metadata",
        "dynamic_groups",
        "jobs",
        "job_buttons",
        "relationship_associations",
        "roles",
        "secrets",
        "secrets_groups",
        "secrets_groups_associations",
        "static_group_associations",
        "statuses",
        "tags",
        "teams",
    ],
    ipam=[
        "ip_addresses",
        "ip_address_to_interface",
        "namespaces",
        "prefixes",
        "prefix_location_assignments",
        "rirs",
        "route_targets",
        "services",
        "vlans",
        "vlan_groups",
        "vlan_location_assignments",
        "vrfs",
        "vrf_device_assignments",
    ],
    plugins=[],
    secrets=[],
    tenancy=["tenants", "tenant_groups"],
    users=["users", "groups", "permissions"],
    virtualization=["cluster_groups", "cluster_types", "clusters", "virtual_machines"],
    wireless=["wireless_networks", "radio_profiles", "supported_data_rates"],
)

# Used to normalize data for the respective query types used to find endpoints
QUERY_TYPES = dict(
    circuit="cid",
    circuit_provider="name",
    circuit_termination="circuit",
    circuit_type="name",
    cloud_network="name",
    cloud_prefix="prefix",
    cloud_provider="name",
    cloud_service="name",
    cluster="name",
    cluster_group="name",
    cluster_type="name",
    controller="name",
    controller_managed_device_group="name",
    device="name",
    device_family="name",
    dynamic_group="name",
    role="name",
    device_type="model",
    export_targets="name",
    group="name",
    groups="name",
    installed_device="name",
    import_targets="name",
    location="name",
    location_prefix="prefix",
    location_type="name",
    manufacturer="name",
    master="name",
    module_bay_template="name",
    module_bay="name",
    module_type="model",
    nat_inside="address",
    nat_outside="address",
    parent_cloud_network="name",
    parent_location="name",
    parent_location_type="name",
    parent_rack_group="name",
    parent_tenant_group="name",
    parent_inventory_item="name",
    power_panel="name",
    power_port="name",
    power_port_template="name",
    platform="name",
    primary_ip="address",
    primary_ip4="address",
    primary_ip6="address",
    rack="name",
    rack_group="name",
    radio_profile="name",
    rear_port="name",
    rear_port_template="name",
    rir="name",
    route_targets="name",
    secret="name",  # noqa: S106
    secrets_group="name",
    secrets_groups_association="name",
    software_version="version",
    software_image_file="image_file_name",
    status="name",
    supported_data_rate="standard",
    tenant="name",
    tenant_group="name",
    time_zone="timezone",
    user="username",
    virtual_chassis="name",
    virtual_machine="name",
    vlan="name",
    vlan_group="name",
    vrf="name",
    wireless_network="name",
)

# Specifies keys within data that need to be converted to ID and the endpoint to be used when queried
CONVERT_TO_ID = {
    "circuit": "circuits",
    "circuit_provider": "providers",
    "circuit_type": "circuit_types",
    "circuit_termination": "circuit_terminations",
    "circuits.circuittermination": "circuit_terminations",
    "cloud_account": "cloud_accounts",
    "cloud_prefix": "prefixes",
    "cloud_provider": "manufacturers",
    "cloud_resource_type": "cloud_resource_types",
    "cloud_network": "cloud_networks",
    "cloud_network_prefix_assignment": "cloud_network_prefix_assignments",
    "cloud_service": "cloud_services",
    "cloud_service_network_assignment": "cloud_service_network_assignments",
    "cluster": "clusters",
    "cluster_group": "cluster_groups",
    "cluster_type": "cluster_types",
    "contacts": "contacts",
    "controller": "controllers",
    "dcim.consoleport": "console_ports",
    "dcim.consoleserverport": "console_server_ports",
    "dcim.frontport": "front_ports",
    "dcim.interface": "interfaces",
    "dcim.powerfeed": "power_feeds",
    "dcim.poweroutlet": "power_outlets",
    "dcim.powerport": "power_ports",
    "dcim.rearport": "rear_ports",
    "device": "devices",
    "device_type": "device_types",
    "dynamic_group": "dynamic_groups",
    "export_targets": "route_targets",
    "group": "tenant_groups",
    "groups": "groups",
    "import_targets": "route_targets",
    "installed_device": "devices",
    "interface": "interfaces",
    "interface_template": "interface_templates",
    "ip_address": "ip_addresses",
    "ip_addresses": "ip_addresses",
    "ipaddresses": "ip_addresses",
    "job": "jobs",
    "lag": "interfaces",
    "location": "locations",
    "location_prefix": "prefixes",
    "location_type": "location_types",
    "manufacturer": "manufacturers",
    "metadata_type": "metadata_types",
    "module_bay_template": "module_bay_templates",
    "module_bay": "module_bays",
    "module_type": "module_types",
    "module": "modules",
    "master": "devices",
    "nat_inside": "ip_addresses",
    "nat_outside": "ip_addresses",
    "namespace": "namespaces",
    "platform": "platforms",
    "parent_device": "devices",
    "parent_module_bay": "module_bays",
    "parent_module": "modules",
    "parent_rack_group": "rack_groups",
    "parent_cloud_network": "cloud_networks",
    "parent_location": "locations",
    "parent_location_type": "location_types",
    "parent_tenant_group": "tenant_groups",
    "parent_inventory_item": "inventory_items",
    "power_panel": "power_panels",
    "power_port": "power_ports",
    "power_port_template": "power_port_templates",
    "primary_ip": "ip_addresses",
    "primary_ip4": "ip_addresses",
    "primary_ip6": "ip_addresses",
    "rack": "racks",
    "rack_group": "rack_groups",
    "rear_port": "rear_ports",
    "rear_port_template": "rear_port_templates",
    "rir": "rirs",
    "role": "roles",
    "route_targets": "route_targets",
    "secret": "secrets",
    "secrets_group": "secrets_groups",
    "services": "services",
    "software_version": "software_versions",
    "software_image_files": "software_image_files",
    "status": "statuses",
    "supported_data_rates": "supported_data_rates",
    "tags": "tags",
    "tagged_vlans": "vlans",
    "teams": "teams",
    "tenant": "tenants",
    "tenant_group": "tenant_groups",
    "termination_a": "interfaces",
    "termination_b": "interfaces",
    "untagged_vlan": "vlans",
    "users": "users",
    "virtual_chassis": "virtual_chassis",
    "virtual_machine": "virtual_machines",
    "vlan": "vlans",
    "vlan_group": "vlan_groups",
    "vm_interface": "interfaces",
    "vrf": "vrfs",
}

ENDPOINT_NAME_MAPPING = {
    "cables": "cable",
    "circuit_terminations": "circuit_termination",
    "circuit_types": "circuit_type",
    "circuits": "circuit",
    "cloud_accounts": "cloud_account",
    "cloud_networks": "cloud_network",
    "cloud_network_prefix_assignments": "cloud_network_prefix_assignment",
    "cloud_resource_types": "cloud_resource_type",
    "cloud_services": "cloud_service",
    "cloud_service_network_assignments": "cloud_service_network_assignment",
    "clusters": "cluster",
    "cluster_groups": "cluster_group",
    "cluster_types": "cluster_type",
    "console_ports": "console_port",
    "console_port_templates": "console_port_template",
    "console_server_ports": "console_server_port",
    "console_server_port_templates": "console_server_port_template",
    "contacts": "contact",
    "controllers": "controller",
    "controller_managed_device_groups": "controller_managed_device_group",
    "custom_fields": "custom_field",
    "custom_field_choices": "custom_field_choice",
    "device_bays": "device_bay",
    "device_bay_templates": "device_bay_template",
    "device_cluster_assignments": "device_cluster_assignment",
    "devices": "device",
    "device_families": "device_family",
    "device_types": "device_type",
    "device_redundancy_groups": "device_redundancy_group",
    "dynamic_groups": "dynamic_group",
    "front_ports": "front_port",
    "front_port_templates": "front_port_template",
    "groups": "group",
    "interfaces": "interface",
    "interface_templates": "interface_template",
    "inventory_items": "inventory_item",
    "ip_addresses": "ip_address",
    "ip_address_to_interface": "ip_address_to_interface",
    "job_buttons": "job_button",
    "locations": "location",
    "location_types": "location_type",
    "manufacturers": "manufacturer",
    "metadata_choices": "metadata_choice",
    "metadata_types": "metadata_type",
    "module_bay_templates": "module_bay_template",
    "module_bays": "module_bay",
    "module_types": "module_type",
    "modules": "module",
    "namespaces": "namespace",
    "object_metadata": "object_metadata",
    "permissions": "permission",
    "platforms": "platform",
    "power_feeds": "power_feed",
    "power_outlets": "power_outlet",
    "power_outlet_templates": "power_outlet_template",
    "power_panels": "power_panel",
    "power_ports": "power_port",
    "power_port_templates": "power_port_template",
    "prefixes": "prefix",
    "prefix_location_assignments": "prefix_location_assignments",
    "providers": "provider",
    "racks": "rack",
    "rack_groups": "rack_group",
    "radio_profiles": "radio_profile",
    "rear_ports": "rear_port",
    "rear_port_templates": "rear_port_template",
    "relationship_associations": "relationship_associations",
    "rirs": "rir",
    "roles": "role",
    "route_targets": "route_target",
    "secrets": "secret",
    "secrets_groups": "secrets_group",
    "secrets_groups_associations": "secrets_groups_association",
    "services": "services",
    "static_group_associations": "static_group_association",
    "software_versions": "software_version",
    "software_image_files": "software_image_file",
    "statuses": "statuses",
    "supported_data_rates": "supported_data_rate",
    "tags": "tags",
    "teams": "team",
    "tenants": "tenant",
    "tenant_groups": "tenant_group",
    "users": "user",
    "virtual_chassis": "virtual_chassis",
    "virtual_machines": "virtual_machine",
    "vlans": "vlan",
    "vlan_groups": "vlan_group",
    "vlan_location_assignments": "vlan_location_assignments",
    "vrfs": "vrf",
    "vrf_device_assignments": "vrf_device_assignments",
    "wireless_networks": "wireless_network",
}

# What makes the search unique
ALLOWED_QUERY_PARAMS = {
    "circuit": set(["cid"]),
    "circuit_type": set(["name"]),
    "circuit_termination": set(["circuit", "term_side"]),
    "circuits.circuittermination": set(["circuit", "term_side"]),
    "cloud_account": set(["name"]),
    "cloud_network": set(["name"]),
    "cloud_network_prefix_assignment": set(["cloud_network", "prefix"]),
    "cloud_resource_type": set(["name"]),
    "cloud_service": set(["name"]),
    "cloud_service_network_assignment": set(["cloud_service", "cloud_network"]),
    "cluster": set(["name", "type"]),
    "cluster_group": set(["name"]),
    "cluster_type": set(["name"]),
    "console_port": set(["name", "device"]),
    "console_port_template": set(["name", "device_type"]),
    "console_server_port": set(["name", "device"]),
    "console_server_port_template": set(["name", "device_type"]),
    "contact": set(["name", "phone", "email"]),
    "contacts": set(["name", "phone", "email"]),
    "controller": set(["name"]),
    "controller_managed_device_group": set(["name"]),
    "custom_field": set(["label"]),
    "custom_field_choice": set(["value", "custom_field"]),
    "dcim.consoleport": set(["name", "device", "module"]),
    "dcim.consoleserverport": set(["name", "device", "module"]),
    "dcim.frontport": set(["name", "device", "module", "rear_port"]),
    "dcim.interface": set(["name", "device", "module", "virtual_machine"]),
    "dcim.powerfeed": set(["name", "power_panel"]),
    "dcim.poweroutlet": set(["name", "device", "module"]),
    "dcim.powerport": set(["name", "device", "module"]),
    "dcim.rearport": set(["name", "device", "module"]),
    "device_bay": set(["name", "device"]),
    "device_bay_template": set(["name", "device_type"]),
    "device_cluster_assignment": set(["device", "cluster"]),
    "device": set(["name", "location", "role", "device_type", "tenant"]),
    "device_family": set(["name"]),
    "device_redundancy_group": set(["name"]),
    "device_type": set(["model"]),
    "dynamic_group": set(["name"]),
    "front_port": set(["name", "device", "module", "rear_port"]),
    "front_port_template": set(["name", "device_type", "rear_port_template"]),
    "group": set(["name"]),
    "groups": set(["name"]),
    "installed_device": set(["name"]),
    "interface": set(["name", "device", "module", "virtual_machine"]),
    "interface_template": set(["name", "device_type"]),
    "inventory_item": set(["name", "device"]),
    "ip_address": set(["address", "namespace", "device", "interfaces", "vm_interfaces"]),
    "ip_addresses": set(["address", "namespace", "device", "interfaces", "vm_interfaces"]),
    "ipaddresses": set(["address", "namespace", "device", "interfaces", "vm_interfaces"]),
    "ip_address_to_interface": set(["ip_address", "interface", "vm_interface"]),
    "job_button": set(["name"]),
    "lag": set(["name"]),
    "location": set(["name", "id", "parent"]),
    "location_prefix": set(["prefix", "namespace"]),
    "location_type": set(["name"]),
    "manufacturer": set(["name"]),
    "master": set(["name"]),
    "metadata_choice": set(["value", "metadata_type"]),
    "metadata_type": set(["name"]),
    "module_bay_template": set(["name", "device_type", "module_type"]),
    "module_bay": set(["name", "parent_device", "parent_module"]),
    "module_type": set(["model"]),
    "module": set(["module_type", "parent_module_bay", "location"]),
    "namespace": set(["name"]),
    "nat_inside": set(["namespace", "address"]),
    "object_metadata": set(["metadata_type", "assigned_object_type", "assigned_object_id", "value"]),
    "parent_location_type": set(["name"]),
    "parent_module_bay": set(["name", "parent_device", "parent_module"]),
    "parent_module": set(["module_type", "parent_module_bay"]),
    "parent_rack_group": set(["name"]),
    "parent_tenant_group": set(["name"]),
    "parent_inventory_item": set(["name", "device"]),
    "permission": set(["name"]),
    "platform": set(["name"]),
    "power_feed": set(["name", "power_panel"]),
    "power_outlet": set(["name", "device"]),
    "power_outlet_template": set(["name", "device_type"]),
    "power_panel": set(["name", "location"]),
    "power_port": set(["name", "device"]),
    "power_port_template": set(["name", "device_type"]),
    "prefix": set(["prefix", "namespace"]),
    "prefix_location_assignments": set(["prefix", "location"]),
    "primary_ip4": set(["address", "namespace"]),
    "primary_ip6": set(["address", "namespace"]),
    "provider": set(["name"]),
    "rack": set(["name", "location"]),
    "rack_group": set(["name"]),
    "radio_profile": set(["name"]),
    "rear_port": set(["name", "device"]),
    "rear_port_template": set(["name", "device_type"]),
    "relationship_associations": set(["source_id", "destination_id"]),
    "rir": set(["name"]),
    "role": set(["name"]),
    "route_target": set(["name"]),
    "secret": set(["name"]),
    "secrets_group": set(["name"]),
    "secrets_groups_association": set(["secrets_group", "secret", "access_type", "secret_type"]),
    "services": set(["device", "virtual_machine", "name", "port", "protocol"]),
    "software_version": set(["version", "platform"]),
    "software_image_file": set(["image_file_name", "software_version"]),
    "software_image_files": set(["image_file_name", "software_version"]),
    "static_group_association": set(["dynamic_group", "associated_object_type", "associated_object_id"]),
    "statuses": set(["name"]),
    "supported_data_rate": set(["standard", "rate"]),
    "supported_data_rates": set(["standard", "rate"]),
    "tags": set(["name"]),
    "tagged_vlans": set(["group", "name", "location", "vid", "vlan_group", "tenant"]),
    "team": set(["name", "phone", "email"]),
    "teams": set(["name", "phone", "email"]),
    "tenant": set(["name"]),
    "tenant_group": set(["name"]),
    "termination_a": set(["name", "device", "virtual_machine"]),
    "termination_b": set(["name", "device", "virtual_machine"]),
    "user": set(["username"]),
    "untagged_vlan": set(["group", "name", "location", "vid", "vlan_group", "tenant"]),
    "virtual_chassis": set(["name", "device"]),
    "virtual_machine": set(["name", "cluster"]),
    "vlan": set(["name", "location", "tenant", "vid", "vlan_group"]),
    "vlan_group": set(["name", "location"]),
    "vlan_location_assignments": set(["vlan", "location"]),
    "vm_interface": set(["name", "virtual_machine"]),
    "vrf": set(["name", "namespace", "rd"]),
    "vrf_device_assignments": set(["vrf", "device", "virtual_machine", "virtual_device_context"]),
    "wireless_network": set(["name"]),
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
        "tenant",
        "type",
        "virtual_machine",
        "vminterface",
    ]
)

# Some API endpoints dropped '_id' in filter fields in 2.0, ignore them here.
IGNORE_ADDING_IDS = {
    "device_bay",
    "device_cluster_assignment",
    "circuit_termination",
    "console_port",
    "console_server_port",
    "front_port",
    "inventory_item",
    "ip_address_to_interface",
    "power_port",
    "power_outlet",
    "rear_port",
    "services",
    "vrf_device_assignments",
    # Cable termination types
    "circuits.circuittermination",
    "dcim.consoleport",
    "dcim.consoleserverport",
    "dcim.frontport",
    "dcim.interface",
    "dcim.powerfeed",
    "dcim.poweroutlet",
    "dcim.powerport",
    "dcim.rearport",
}

# This is used to standardize choice fields to a single value
# (e.g. {"display": "Foo", "value": "foo"} => "foo").
CONVERT_CHOICES = {
    "cables": set(["termination_a_type", "termination_b_type", "type", "length_unit"]),
    "console_ports": set(["type"]),
    "console_port_templates": set(["type"]),
    "console_server_ports": set(["type"]),
    "console_server_port_templates": set(["type"]),
    "devices": set(["face"]),
    "device_types": set(["subdevice_role"]),
    "front_ports": set(["type"]),
    "front_port_templates": set(["type"]),
    "interfaces": set(["form_factor", "mode", "type"]),
    "interface_templates": set(["type"]),
    "ip_addresses": set(["type"]),
    "prefixes": set(["type"]),
    "power_feeds": set(["type", "supply", "phase"]),
    "power_outlets": set(["type", "feed_leg"]),
    "power_outlet_templates": set(["type", "feed_leg"]),
    "power_ports": set(["type"]),
    "power_port_templates": set(["type"]),
    "racks": set(["outer_unit", "type"]),
    "radio_profiles": set(["channel_width"]),
    "rear_ports": set(["type"]),
    "rear_port_templates": set(["type"]),
    "services": set(["protocol"]),
    "virtual_machines": set(["face"]),
}

# This is used to map non-clashing keys to Nautobot API compliant keys to prevent bad logic in code for similar keys but different modules
CONVERT_KEYS = {
    "circuit_provider": "provider",
    "cloud_prefix": "prefix",
    "cloud_provider": "provider",
    "location_prefix": "prefix",
    "parent_cloud_network": "parent",
    "parent_rack_group": "parent",
    "parent_location": "parent",
    "parent_location_type": "parent",
    "parent_tenant_group": "parent",
    "parent_inventory_item": "parent",
    "rear_port_template_position": "rear_port_position",
    "termination_a": "termination_a_id",
    "termination_b": "termination_b_id",
}


# Options not sent for filtering
NAUTOBOT_ARG_SPEC = dict(
    url=dict(type="str", required=True, fallback=(env_fallback, ["NAUTOBOT_URL"])),
    token=dict(type="str", required=True, no_log=True, fallback=(env_fallback, ["NAUTOBOT_TOKEN"])),
    state=dict(required=False, default="present", choices=["present", "absent"]),
    query_params=dict(required=False, type="list", elements="str"),
    validate_certs=dict(type="raw", default=True, fallback=(env_fallback, ["NAUTOBOT_VALIDATE_CERTS"])),
    api_version=dict(type="str", required=False),
)

ID_ARG_SPEC = dict(
    id=dict(type="str", required=False),
)

TAGS_ARG_SPEC = dict(
    tags=dict(required=False, type="list", elements="raw"),
)

CUSTOM_FIELDS_ARG_SPEC = dict(
    custom_fields=dict(required=False, type="dict"),
)


def check_needs_wrapping(value):
    """Recursively checks lists and dictionaries, and checks strings directly, to see if they need to be wrapped due to containing Jinja2 delimiters."""
    if isinstance(value, str):
        return "{{" in value or "{%" in value
    elif isinstance(value, dict):
        return any(check_needs_wrapping(v) for v in value.values())
    elif isinstance(value, list):
        return any(check_needs_wrapping(item) for item in value)
    return False


def is_truthy(arg):
    """
    Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True

    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg

    val = str(arg).lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truthy value: `{arg}`")


def sort_dict_with_lists(data):
    """Recursively sort a dictionary with lists for better comparison."""
    if isinstance(data, dict):
        return {k: sort_dict_with_lists(v) for k, v in sorted(data.items())}
    if isinstance(data, list):
        return sorted([sort_dict_with_lists(v) for v in data], key=lambda x: json.dumps(x, sort_keys=True))
    return data


class NautobotModule:
    """Run the Nautobot module.

    Initialize connection to Nautobot, sets AnsibleModule passed in to
    self.module to be used throughout the class
    :params module (obj): Ansible Module object
    :params endpoint (str): Used to tell class which endpoint the logic needs to follow
    :params nb_client (obj): pynautobot.api object passed in (not required)
    """

    def __init__(self, module, endpoint, client=None, remove_keys=None):
        """Initialize the Nautobot module."""
        self.module = module
        self.state = self.module.params["state"]
        self.check_mode = self.module.check_mode
        self.endpoint = endpoint
        query_params = self.module.params.get("query_params")

        if not HAS_PYNAUTOBOT:
            self.module.fail_json(msg=missing_required_lib("pynautobot"), exception=PYNAUTOBOT_IMP_ERR)
        # These should not be required after making connection to Nautobot
        url = self.module.params["url"]
        token = self.module.params["token"]
        ssl_verify = self.module.params["validate_certs"]
        api_version = self.module.params["api_version"]

        # Attempt to initiate connection to Nautobot
        if client is None:
            self.nb = self._connect_api(url, token, ssl_verify, api_version)
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
            greater_or_equal (bool): If True, return True if the major version is equal and the minor version is greater or equal
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

    def _connect_api(self, url, token, ssl_verify, api_version):
        try:
            # nb = pynautobot.api(url, token=token, api_version=api_version, verify=ssl_verify)
            nb = pynautobot.api(url, token=token, api_version=api_version, verify=ssl_verify, exclude_m2m=False)
            self.version = nb.version
            return nb
        except pynautobot.RequestError as e:
            self._handle_errors(msg=e.error)
        except ValueError as e:
            # pynautobot 2.0 does version constraint on init, handle errors if versions doesn't match.
            self._handle_errors(msg=str(e))
        except Exception:
            self.module.fail_json(msg="Failed to establish connection to Nautobot API")

    def _nb_endpoint_get(self, nb_endpoint, query_params, search_item):
        try:
            response = nb_endpoint.get(**query_params)
        except pynautobot.RequestError as e:
            self._handle_errors(msg=e.error)
        except ValueError:
            self._handle_errors(msg="More than one result returned for %s" % (search_item))

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
            self._handle_errors(msg="Incorrect encoding of fetched payload from Nautobot API.")

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
            self._handle_errors("The following query_params are invalid: {0}".format(", ".join(invalid_query_params)))

    def _handle_errors(self, msg):
        """
        Returns message and changed = False.

        :params msg (str): Message indicating why there is no change
        """
        self.module.fail_json(msg=msg, changed=False)

    def _build_diff(self, before=None, after=None):
        """Builds diff of before and after changes."""
        return {"before": before, "after": after}

    def _convert_identical_keys(self, data):
        """Convert non-clashing keys for each module into identical keys that are required.

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
                new_key = CONVERT_KEYS[key]
                temp_dict[new_key] = data[key]
            else:
                temp_dict[key] = data[key]

        return temp_dict

    def _remove_arg_spec_default(self, data):
        """Remove any data keys that were not provided by user, but has the arg spec.

        Used to remove any data keys that were not provided by user, but has the arg spec
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
        """Find IDs of necessary searches when required under _build_query_params.

        Used to find IDs of necessary searches when required under _build_query_params
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
            # Inherited django models(admin groups) that are not overloaded are integers, force the integer to string.
            return str(result.id)
        else:
            return data

    def _build_query_params(self, parent, module_data, user_query_params=None, child=None):
        """Build a query dictionary for Nautobot endpoints.

        :returns dict(query_dict): Returns a query dictionary built using mappings to dynamically
        build available query params for Nautobot endpoints
        :params parent(str): This is either a key from `_find_ids` or a string passed in to determine
        which keys in the data that we need to use to construct `query_dict`
        :params module_data(dict): Uses the data provided to the Nautobot module
        :params child(dict): This is used within `_find_ids` and passes the inner dictionary
        to build the appropriate `query_dict` for the parent
        """
        # If they provided the ID, it's the only query param we need
        if module_data.get("id"):
            return {"id": module_data["id"]}

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
            if match in QUERY_PARAMS_IDS and parent not in IGNORE_ADDING_IDS:
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
            intf_type = self._fetch_choice_value("Link Aggregation Group (LAG)", "interfaces")
            query_dict.update({"type": intf_type})
            if isinstance(module_data["device"], int) or self.is_valid_uuid(module_data["device"]):
                query_dict.update({"device_id": module_data["device"]})
            else:
                query_dict.update({"device": module_data["device"]})

        elif parent == "prefix" and module_data.get("parent"):
            query_dict.update({"prefix": module_data["parent"]})

        elif parent == "ip_addresses":
            if isinstance(module_data["device"], int) or self.is_valid_uuid(module_data["device"]):
                query_dict.update({"device_id": module_data["device"]})
            else:
                query_dict.update({"device": module_data["device"]})

        elif parent == "rear_port" and self.endpoint == "front_ports":
            if isinstance(module_data.get("rear_port"), str):
                rear_port = {
                    "name": module_data.get("rear_port"),
                }
                query_dict.update(rear_port)

        elif parent == "rear_port_template" and self.endpoint == "front_port_templates":
            if isinstance(module_data.get("rear_port_template"), str):
                rear_port_template = {
                    "name": module_data.get("rear_port_template"),
                }
                query_dict.update(rear_port_template)

        if not query_dict:
            provided_kwargs = child.keys() if child else module_data.keys()
            acceptable_query_params = user_query_params if user_query_params else query_params
            self._handle_errors(
                f"One or more of the kwargs provided are invalid for {parent},"
                f" provided kwargs: {', '.join(sorted(provided_kwargs))}. Acceptable kwargs: {', '.join(sorted(acceptable_query_params))}"
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
                msg="Failed to fetch endpoint choices to validate against. This requires a write-enabled token. Make "
                "sure the token is write-enabled. If looking to fetch only information, use either the inventory or lookup plugin."
            )

        choices = list(chain.from_iterable(endpoint_choices.values()))

        search_term = search.lower() if isinstance(search, str) else search
        for item in choices:
            if item["display"].lower() == search_term:
                return item["value"]
            if item["value"] == search_term:
                return item["value"]
        valid_choices = [choice["value"] for choice in choices]
        self._handle_errors(
            msg=f"{search} was not found as a valid choice for {endpoint}, valid choices are: {valid_choices}"
        )

    def _change_choices_id(self, endpoint, data):
        """Change data that is static and under _choices for the application.

        Used to change data that is static and under _choices for the application.
        ex. DEVICE_STATUS
        :returns data (dict): Returns the user defined data back with updated fields for _choices
        :params endpoint (str): The endpoint that will be used for mapping to required _choices
        :params data (dict): User defined data passed into the module
        """
        if CONVERT_CHOICES.get(endpoint):
            required_choices = CONVERT_CHOICES[endpoint]
            for choice in required_choices:
                if data.get(choice):
                    if isinstance(data[choice], int) or self.is_valid_uuid(data[choice]):
                        continue
                    if isinstance(data[choice], list):
                        data[choice] = [self._fetch_choice_value(item, endpoint) for item in data[choice]]
                    else:
                        data[choice] = self._fetch_choice_value(data[choice], endpoint)

        return data

    def _find_app(self, endpoint):
        """Finds the application of the endpoint passed in.

        Dynamically finds application of endpoint passed in using the
        API_APPS_ENDPOINTS for mapping
        :returns nb_app (str): The application the endpoint lives under
        :params endpoint (str): The endpoint requiring resolution to application
        """
        for k, v in API_APPS_ENDPOINTS.items():
            if endpoint in v:
                nb_app = k
        return nb_app

    def _find_ids(self, data, user_query_params):
        """Find the IDs of all user specified data if resolvable.

        :returns data (dict): Returns the updated dict with the IDs of user specified data
        :params data (dict): User defined data passed into the module
        """
        for k, v in data.items():
            if k in CONVERT_TO_ID:
                # Do not attempt to resolve if already ID/UUID is provided
                if isinstance(v, int) or self.is_valid_uuid(v):
                    continue
                # Special circumstances to set endpoint to search within
                elif k == "termination_a":
                    endpoint = CONVERT_TO_ID[data.get("termination_a_type")]
                elif k == "termination_b":
                    endpoint = CONVERT_TO_ID[data.get("termination_b_type")]
                else:
                    endpoint = CONVERT_TO_ID[k]
                search = v
                app = self._find_app(endpoint)
                nb_app = getattr(self.nb, app)
                nb_endpoint = getattr(nb_app, endpoint)

                if isinstance(v, dict):
                    if k == "vm_interface" and v.get("virtual_machine"):
                        nb_app = getattr(self.nb, "virtualization")
                        nb_endpoint = getattr(nb_app, endpoint)
                    query_params = self._build_query_params(k, data, child=v)
                    query_id = self._nb_endpoint_get(nb_endpoint, query_params, k)
                elif isinstance(v, list):
                    id_list = list()
                    for list_item in v:
                        if k == "tags" and isinstance(list_item, str) and not self.is_valid_uuid(list_item):
                            temp_dict = {"name": list_item}
                        elif isinstance(list_item, dict):
                            norm_data = self._normalize_data(list_item)
                            temp_dict = self._build_query_params(k, data, child=norm_data)
                        # If user passes in an integer, add to ID list to id_list as user
                        # should have passed in a tag ID
                        elif isinstance(list_item, int) or self.is_valid_uuid(list_item):
                            id_list.append(list_item)
                            continue
                        else:
                            # Reminder: this get checks the QUERY_TYPES constant above, if the item is not in the list
                            # of approved query types, then it defaults to a q search
                            temp_dict = {QUERY_TYPES.get(k, "q"): list_item}

                        query_id = self._nb_endpoint_get(nb_endpoint, temp_dict, k)
                        if query_id:
                            id_list.append(query_id.id)
                        else:
                            self._handle_errors(msg="%s not found" % (list_item))
                else:
                    if k in ["lag", "rear_port", "rear_port_template"]:
                        query_params = self._build_query_params(k, data, user_query_params)
                    else:
                        # Reminder: this get checks the QUERY_TYPES constant above, if the item is not in the list
                        # of approved query types, then it defaults to a q search
                        query_params = {QUERY_TYPES.get(k, "q"): search}
                    query_id = self._nb_endpoint_get(nb_endpoint, query_params, k)

                if isinstance(v, list):
                    data[k] = id_list
                elif query_id:
                    data[k] = query_id.id
                else:
                    self._handle_errors(msg="Could not resolve id of %s: %s" % (k, v))

        return data

    def _normalize_data(self, data):
        """Normalize module data to formats accepted by Nautobot searches.

        :returns data (dict): Normalized module data to formats accepted by Nautobot searches
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

            else:
                data_type = QUERY_TYPES.get(k, "q")
                if data_type == "timezone":
                    if " " in v:
                        data[k] = v.replace(" ", "_")
            if k == "description":
                data[k] = v.strip()

            if k == "mac_address":
                data[k] = v.upper()

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
                if isinstance(nb_endpoint, pynautobot.core.endpoint.DetailEndpoint):
                    nb_obj = nb_endpoint.create(data)
                else:
                    nb_obj = nb_endpoint.create(**data)
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
        if "custom_fields" in serialized_nb_obj:
            custom_fields = serialized_nb_obj.get("custom_fields", {})
            shared_keys = custom_fields.keys() & data.get("custom_fields", {}).keys()
            serialized_nb_obj["custom_fields"] = {
                key: custom_fields[key] for key in shared_keys if custom_fields[key] is not None
            }
        updated_obj = serialized_nb_obj.copy()
        updated_obj.update(data)
        if serialized_nb_obj.get("tags") and data.get("tags"):
            serialized_nb_obj["tags"] = set(serialized_nb_obj["tags"])
            updated_obj["tags"] = set(data["tags"])

        if sort_dict_with_lists(serialized_nb_obj) == sort_dict_with_lists(updated_obj):
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
                        msg = "form_factor is not valid. Please use the type key instead."
                    else:
                        msg = "%s does not exist on existing object. Check to make sure valid field." % (key)

                    self._handle_errors(msg=msg)

            if not self.check_mode:
                self.nb_object.update(data)
                updated_obj = self.nb_object.serialize()

            diff = self._build_diff(before=data_before, after=data_after)
            return updated_obj, diff

    def _ensure_object_exists(self, nb_endpoint, endpoint_name, name, data):
        """Ensure an object exists or is updated.

        Used when `state` is present to make sure object exists or if the object exists
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
                self._handle_errors(msg="Request failed, couldn't update object: %s" % name)
            if diff:
                self.result["msg"] = "%s %s updated" % (endpoint_name, name)
                self.result["changed"] = True
                self.result["diff"] = diff
            else:
                self.result["msg"] = "%s %s already exists" % (endpoint_name, name)

    def _ensure_object_absent(self, endpoint_name, name):
        """Ensure an object is absent.

        Used when `state` is absent to make sure object does not exist
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
        Must be implemented in subclasses.
        """
        raise NotImplementedError


class NautobotApiBase:
    def __init__(self, **kwargs):
        """Initialize the Nautobot API base."""
        self.url = kwargs.get("url") or os.getenv("NAUTOBOT_URL")
        self.token = kwargs.get("token") or os.getenv("NAUTOBOT_TOKEN")
        if kwargs.get("ssl_verify") is not None:
            self.ssl_verify = kwargs.get("ssl_verify")
        elif os.getenv("NAUTOBOT_VALIDATE_CERTS") is not None:
            self.ssl_verify = is_truthy(os.getenv("NAUTOBOT_VALIDATE_CERTS"))
        else:
            self.ssl_verify = True
        self.api_version = kwargs.get("api_version")

        # Setup the API client calls
        self.api = pynautobot.api(
            url=self.url,
            token=self.token,
            api_version=self.api_version,
            verify=self.ssl_verify,
            exclude_m2m=False,
        )


class NautobotGraphQL:
    def __init__(self, query_str, api=None, variables=None):
        """Initialize the Nautobot GraphQL class."""
        self.query_str = query_str
        self.pynautobot = api.api
        self.variables = variables

    def query(self):
        """Makes API call and checks response from GraphQL endpoint."""
        # Make API call to query
        graph_response = self.pynautobot.graphql.query(query=self.query_str, variables=self.variables)

        return graph_response
