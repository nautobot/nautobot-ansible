#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys
import pynautobot
from packaging import version

# NOTE: If anything depends on specific versions of Nautobot, can check INTEGRATION_TESTS in env
# os.environ["INTEGRATION_TESTS"]


# Set nb variable to connect to Nautobot and use the veriable in future calls
nb_host = os.getenv("NAUTOBOT_URL", "http://nautobot:8000")
nb_token = os.getenv("NAUTOBOT_TOKEN", "0123456789abcdef0123456789abcdef01234567")
nb = pynautobot.api(nb_host, nb_token)
api_version = version.parse(nb.version)

# Set the nautobot version for conditional population of data
nb_status = nb.status()
nautobot_version = version.parse(nb_status["nautobot-version"])

ERRORS = False


def make_nautobot_calls(endpoint, payload):
    """Make the necessary calls to create endpoints, and pass any errors.

    Args:
        endpoint (obj): pynautobot endpoint object.
        payload (list): List of endpoint objects.
    """
    try:
        created = endpoint.create(payload)
    except pynautobot.RequestError as e:
        print(e.error)
        ERRORS = True
        return

    return created


# Create tags used in future tests
create_tags = make_nautobot_calls(
    nb.extras.tags,
    [
        {"name": "First", "content_types": ["dcim.device"]},
        {"name": "Second", "content_types": ["dcim.device"]},
        {"name": "Third", "content_types": ["dcim.device"]},
        {"name": "Schnozzberry", "content_types": ["dcim.device"]},
        {"name": "Lookup", "content_types": ["dcim.device"]},
        {"name": "Nolookup", "content_types": ["dcim.device"]},
        {"name": "tagA", "content_types": ["dcim.device"]},
        {"name": "tagB", "content_types": ["dcim.device"]},
        {"name": "tagC", "content_types": ["dcim.device"]},
        {"name": "Updated", "content_types": ["dcim.device"]},
    ],
)

# ORDER OF OPERATIONS FOR THE MOST PART
# Create TENANT GROUPS
tenant_groups = [{"name": "test-tenant-group"}]
created_tenant_groups = make_nautobot_calls(nb.tenancy.tenant_groups, tenant_groups)
test_tenant_group = nb.tenancy.tenant_groups.get(name="test-tenant-group")

# Create TENANTS
tenants = [{"name": "test-tenant", "group": test_tenant_group.id}]
created_tenants = make_nautobot_calls(nb.tenancy.tenants, tenants)
# Test Tenant to be used later on
test_tenant = nb.tenancy.tenants.get(name="test-tenant")

# Create location types
location_content_types = [
    "dcim.device",
    "dcim.rack",
    "dcim.rackgroup",
    "dcim.powerpanel",
    "ipam.prefix",
    "ipam.vlangroup",
    "ipam.vlan",
    "virtualization.cluster",
    "circuits.circuittermination",
]
location_types = [{"name": "my-parent-location-type", "content_types": location_content_types, "nestable": True}]
created_location_types = make_nautobot_calls(nb.dcim.location_types, location_types)
parent_location_type = nb.dcim.location_types.get(name="my-parent-location-type")

# Create child location types
child_location_types = [
    {
        "name": "my-child-location-type",
        "content_types": location_content_types,
        "nestable": True,
        "parent": parent_location_type.id,
    }
]
created_child_location_types = make_nautobot_calls(nb.dcim.location_types, child_location_types)
child_location_type = nb.dcim.location_types.get(name="my-child-location-type")

# Create locations
parent_location_attrs = [
    {"name": "parent-test-location", "location_type": parent_location_type.id, "tenant": test_tenant.id, "status": {"name": "Active"}},
]
make_nautobot_calls(nb.dcim.locations, parent_location_attrs)

# Location variables to be used later on
location_parent = nb.dcim.locations.get(name="parent-test-location")
child_location_attrs = [
    {"name": "child-test-location", "location_type": child_location_type.id, "parent": location_parent.id, "status": {"name": "Active"}},
]
make_nautobot_calls(nb.dcim.locations, child_location_attrs)
location_child = nb.dcim.locations.get(name="child-test-location")

# Create power panel
power_panels = [{"name": "test-power-panel", "location": location_parent.id}]
created_power_panels = make_nautobot_calls(nb.dcim.power_panels, power_panels)

# Create VRFs
vrfs = [{"name": "test-vrf", "rd": "1:1", "namespace": {"name": "Global"}}]
created_vrfs = make_nautobot_calls(nb.ipam.vrfs, vrfs)


# Create PREFIXES
prefixes = [
    {"prefix": "192.168.0.0/16", "location": location_parent.id, "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "10.0.0.0/8", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "172.16.0.0/12", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "2001::1:0/64", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
]
created_prefixes = make_nautobot_calls(nb.ipam.prefixes, prefixes)


# Create VLAN GROUPS
vlan_groups = [
    {"name": "test-vlan-group", "location": location_parent.id, "tenant": test_tenant.id},
    {"name": "test-vlan-group-2", "location": location_parent.id, "tenant": test_tenant.id},
]
created_vlan_groups = make_nautobot_calls(nb.ipam.vlan_groups, vlan_groups)
# VLAN Group variables to be used later on
test_vlan_group = nb.ipam.vlan_groups.get(name="test-vlan-group")


# Create VLANS
vlans = [
    {"name": "Wireless", "vid": 100, "location": location_parent.id, "status": {"name": "Active"}},
    {"name": "Data", "vid": 200, "location": location_parent.id, "status": {"name": "Active"}},
    {"name": "VoIP", "vid": 300, "location": location_parent.id, "status": {"name": "Active"}},
    {
        "name": "Test VLAN",
        "vid": 400,
        "location": location_parent.id,
        "tenant": test_tenant.id,
        "group": test_vlan_group.id,
        "status": {"name": "Active"},
    },
]
created_vlans = make_nautobot_calls(nb.ipam.vlans, vlans)


# Create IPAM Roles
ipam_roles = [{"name": "network-of-care", "content_types": ["ipam.prefix"]}]
create_ipam_roles = make_nautobot_calls(nb.extras.roles, ipam_roles)


# Create Manufacturers
manufacturers = [
    {"name": "Cisco"},
    {"name": "Arista"},
    {"name": "test-manufacturer"},
]
created_manufacturers = make_nautobot_calls(nb.dcim.manufacturers, manufacturers)
# Manufacturer variables to be used later on
cisco_manu = nb.dcim.manufacturers.get(name="Cisco")
arista_manu = nb.dcim.manufacturers.get(name="Arista")


# Create Device Types
device_types = [
    {"model": "cisco-test", "manufacturer": cisco_manu.id},
    {"model": "arista-test", "manufacturer": arista_manu.id},
    {
        "model": "nexus-parent",
        "u_height": 0,
        "manufacturer": cisco_manu.id,
        "subdevice_role": "parent",
    },
    {
        "model": "nexus-child",
        "u_height": 0,
        "manufacturer": cisco_manu.id,
        "subdevice_role": "child",
    },
    {"model": "1841", "manufacturer": cisco_manu.id},
]

created_device_types = make_nautobot_calls(nb.dcim.device_types, device_types)
# Device type variables to be used later on
cisco_test = nb.dcim.device_types.get(model="cisco-test")
arista_test = nb.dcim.device_types.get(model="arista-test")
nexus_parent = nb.dcim.device_types.get(model="nexus-parent")
nexus_child = nb.dcim.device_types.get(model="nexus-child")

# Create Rear Port Template
rear_port_templates = [{"name": "test-rear-port-template", "device_type": cisco_test.id, "type": "bnc", "positions": 5}]
created_rear_port_templates = make_nautobot_calls(nb.dcim.rear_port_templates, rear_port_templates)

# Create Device Roles
device_roles = [
    {"name": "core-switch", "color": "aa1409", "vm_role": False, "content_types": ["dcim.device"]},
    {"name": "test-vm-role", "color": "e91e63", "vm_role": True, "content_types": ["dcim.device"]},
    {"name": "test-vm-role-1", "color": "e91e65", "vm_role": True, "content_types": ["dcim.device"]},
]
created_device_roles = make_nautobot_calls(nb.extras.roles, device_roles)
# Device role variables to be used later on
core_switch = nb.extras.roles.get(name="core-switch")


# Create Rack Groups
rack_groups = [
    {"name": "test-rack-group", "location": location_parent.id},
    {"name": "parent-rack-group", "location": location_parent.id},
]
created_rack_groups = make_nautobot_calls(nb.dcim.rack_groups, rack_groups)

rack_group1 = nb.dcim.rack_groups.get(name="test-rack-group")
rack_group2 = nb.dcim.rack_groups.get(name="parent-rack-group")
# Create Rack Group Parent relationship
rack_group1.parent = rack_group2.id
rack_group1.save()

# Create Rack Roles
rack_roles = [{"name": "test-rack-role", "color": "4287f5", "content_types": ["dcim.rack"]}]
created_rack_roles = make_nautobot_calls(nb.extras.roles, rack_roles)
rack_role1 = nb.extras.roles.get(name="test-rack-role")

# Create Racks
racks = [
    {"name": "test-rack-site-2", "rack_group": rack_group2.id, "location": location_child.id, "role": rack_role1.id, "status": {"name": "Active"}},
    {"name": "test-rack", "location": location_parent.id, "rack_group": rack_group1.id, "role": rack_role1.id, "status": {"name": "Active"}},
]
created_racks = make_nautobot_calls(nb.dcim.racks, racks)
test_rack = nb.dcim.racks.get(name="test-rack")
test_rack_site2 = nb.dcim.racks.get(name="test-rack-site-2")


# Create Devices
devices = [
    {
        "name": "test100",
        "device_type": cisco_test.id,
        "role": core_switch.id,
        "location": location_parent.id,
        "tenant": test_tenant.id,
        "local_config_context_data": {"ntp_servers": ["pool.ntp.org"]},
        "status": {"name": "Active"},
    },
    {
        "name": "TestDeviceR1",
        "device_type": cisco_test.id,
        "role": core_switch.id,
        "location": location_parent.id,
        "rack": test_rack.id,
        "status": {"name": "Active"},
    },
    {
        "name": "R1-Device",
        "device_type": cisco_test.id,
        "role": core_switch.id,
        "location": location_child.id,
        "rack": test_rack_site2.id,
        "status": {"name": "Active"},
    },
    {
        "name": "Test-Nexus-One",
        "device_type": nexus_parent.id,
        "role": core_switch.id,
        "location": location_parent.id,
        "status": {"name": "Active"},
    },
    {
        "name": "Test-Nexus-Child-One",
        "device_type": nexus_child.id,
        "role": core_switch.id,
        "location": location_parent.id,
        "status": {"name": "Active"},
    },
]
created_devices = make_nautobot_calls(nb.dcim.devices, devices)
# Device variables to be used later on
test100 = nb.dcim.devices.get(name="test100")

# Create rear port
rear_ports = [{"name": "test-rear-port", "device": test100.id, "type": "bnc", "positions": 5}]
created_rear_ports = make_nautobot_calls(nb.dcim.rear_ports, rear_ports)

# Create power ports
power_ports = [{"name": "test-power-port", "device": test100.id}]
created_power_ports = make_nautobot_calls(nb.dcim.power_ports, power_ports)

# Create console ports
console_ports = [{"name": "test-console-port", "device": test100.id}]
created_console_ports = make_nautobot_calls(nb.dcim.console_ports, console_ports)

# Create console server ports
console_server_ports = [{"name": "test-console-server-port", "device": test100.id}]
created_console_server_ports = make_nautobot_calls(nb.dcim.console_server_ports, console_server_ports)

# Create VC, assign member, create initial interface
nexus = nb.dcim.devices.get(name="Test-Nexus-One")
created_vcs = make_nautobot_calls(nb.dcim.virtual_chassis, {"name": "VC1", "master": nexus.id})
vc = nb.dcim.virtual_chassis.get(name="VC1")
nexus_child = nb.dcim.devices.get(name="Test-Nexus-Child-One")
nexus_child.update({"virtual_chassis": vc.id, "vc_position": 2})
nexus.update({"vc_position": 0})
nexus_interfaces = [
    {"device": nexus.id, "name": "Ethernet1/1", "type": "1000base-t", "status": {"name": "Active"}},
    {"device": nexus_child.id, "name": "Ethernet2/1", "type": "1000base-t", "status": {"name": "Active"}},
]
created_nexus_interfaces = make_nautobot_calls(nb.dcim.interfaces, nexus_interfaces)

# Create Interfaces
dev_interfaces = [
    {"name": "GigabitEthernet1", "device": test100.id, "type": "1000base-t", "status": {"name": "Active"}},
    {"name": "GigabitEthernet2", "device": test100.id, "type": "1000base-t", "status": {"name": "Active"}},
]
created_interfaces = make_nautobot_calls(nb.dcim.interfaces, dev_interfaces)
nexus_eth1 = nb.dcim.interfaces.get(device_id=nexus.id, name="Ethernet1/1")
nexus_child_eth1 = nb.dcim.interfaces.get(device_id=nexus_child.id, name="Ethernet2/1")

# Interface variables to be used later on
test100_gi1 = nb.dcim.interfaces.get(name="GigabitEthernet1", device_id=test100.id)
test100_gi2 = nb.dcim.interfaces.get(name="GigabitEthernet2", device_id=test100.id)


# Create IP Addresses
ip_addresses = [
    {
        "address": "172.16.180.1/24",
        # "assigned_object_type": "dcim.interface",  # TODO find a way to update that via API, looks like M2M is read-only
        # "assigned_object_id": test100_gi1.id,
        "namespace": {"name": "Global"},
        "status": {"name": "Active"},
    },
    {
        "address": "2001::1:1/64",
        # "assigned_object_type": "dcim.interface",  # TODO as above
        # "assigned_object_id": test100_gi2.id,
        "namespace": {"name": "Global"},
        "status": {"name": "Active"},
    },
    {
        "address": "172.16.180.11/24",
        "dns_name": "nexus.example.com",
        # "assigned_object_type": "dcim.interface",  # TODO as above
        # "assigned_object_id": nexus_eth1.id,
        "namespace": {"name": "Global"},
        "status": {"name": "Active"},
    },
    {
        "address": "172.16.180.12/24",
        # "assigned_object_type": "dcim.interface",  # TODO as above
        # "assigned_object_id": nexus_child_eth1.id,
        "namespace": {"name": "Global"},
        "dns_name": "nexus.example.com",
        "status": {"name": "Active"},
    },
    {"address": "172.16.180.254/24", "namespace": {"name": "Global"}, "status": {"name": "Active"}},
]

created_ip_addresses = make_nautobot_calls(nb.ipam.ip_addresses, ip_addresses)
# Grab first two IPs
ip1 = nb.ipam.ip_addresses.get(address="172.16.180.1/24")  # , interface_id=test100_gi1.id) TODO as above
ip2 = nb.ipam.ip_addresses.get(address="2001::1:1/64")  # , interface_id=test100_gi2.id) TODO as above

# Assign Primary IP
nexus_eth1_ip = nb.ipam.ip_addresses.get(address="172.16.180.11/24")  # , interface_id=nexus_eth1.id) TODO as above
# nexus.update({"primary_ip4": nexus_eth1_ip})  # TODO as above

# Create RIRs
rirs = [{"name": "example-rir"}]
created_rirs = make_nautobot_calls(nb.ipam.rirs, rirs)

# Create Cluster Group
cluster_groups = [{"name": "test-cluster-group"}]
created_cluster_groups = make_nautobot_calls(nb.virtualization.cluster_groups, cluster_groups)
test_cluster_group = nb.virtualization.cluster_groups.get(name="test-cluster-group")

# Create Cluster Type
cluster_types = [{"name": "test-cluster-type"}]
created_cluster_types = make_nautobot_calls(nb.virtualization.cluster_types, cluster_types)
test_cluster_type = nb.virtualization.cluster_types.get(name="test-cluster-type")

# Create Cluster
clusters = [
    {"name": "test-cluster", "cluster_type": test_cluster_type.id, "cluster_group": test_cluster_group.id, "location": location_parent.id},
    {"name": "test-cluster-2", "cluster_type": test_cluster_type.id},
]
created_clusters = make_nautobot_calls(nb.virtualization.clusters, clusters)
test_cluster = nb.virtualization.clusters.get(name="test-cluster")
test_cluster2 = nb.virtualization.clusters.get(name="test-cluster-2")

# Create Virtual Machine
virtual_machines = [
    {"name": "test100-vm", "cluster": test_cluster.id, "status": {"name": "Active"}},
    {"name": "test101-vm", "cluster": test_cluster.id, "status": {"name": "Active"}},
    {"name": "test102-vm", "cluster": test_cluster.id, "status": {"name": "Active"}},
    {"name": "test103-vm", "cluster": test_cluster.id, "status": {"name": "Active"}},
    {"name": "test104-vm", "cluster": test_cluster2.id, "status": {"name": "Active"}},
    {"name": "Test VM With Spaces", "cluster": test_cluster2.id, "status": {"name": "Active"}},
]
created_virtual_machines = make_nautobot_calls(nb.virtualization.virtual_machines, virtual_machines)
test100_vm = nb.virtualization.virtual_machines.get(name="test100-vm")
test101_vm = nb.virtualization.virtual_machines.get(name="test101-vm")
test_spaces_vm = nb.virtualization.virtual_machines.get(name="Test VM With Spaces")

# Create Virtual Machine Interfaces
virtual_machines_intfs = [
    # Create test100-vm intfs
    {"name": "Eth0", "virtual_machine": test100_vm.id, "status": {"name": "Active"}},
    {"name": "Eth1", "virtual_machine": test100_vm.id, "status": {"name": "Active"}},
    {"name": "Eth2", "virtual_machine": test100_vm.id, "status": {"name": "Active"}},
    {"name": "Eth3", "virtual_machine": test100_vm.id, "status": {"name": "Active"}},
    {"name": "Eth4", "virtual_machine": test100_vm.id, "status": {"name": "Active"}},
    # Create test101-vm intfs
    {"name": "Eth0", "virtual_machine": test101_vm.id, "status": {"name": "Active"}},
    {"name": "Eth1", "virtual_machine": test101_vm.id, "status": {"name": "Active"}},
    {"name": "Eth2", "virtual_machine": test101_vm.id, "status": {"name": "Active"}},
    {"name": "Eth3", "virtual_machine": test101_vm.id, "status": {"name": "Active"}},
    {"name": "Eth4", "virtual_machine": test101_vm.id, "status": {"name": "Active"}},
    # Create Test VM With Spaces intfs
    {"name": "Eth0", "virtual_machine": test_spaces_vm.id, "status": {"name": "Active"}},
    {"name": "Eth1", "virtual_machine": test_spaces_vm.id, "status": {"name": "Active"}},
]
created_virtual_machines_intfs = make_nautobot_calls(nb.virtualization.interfaces, virtual_machines_intfs)


# Create Services
services = [
    {"device": test100.id, "name": "ssh", "ports": [22], "protocol": "tcp"},
    {"device": test100.id, "name": "http", "ports": [80], "protocol": "tcp", "ipaddresses": [ip1.id, ip2.id]},
    {"device": nexus.id, "name": "telnet", "ports": [23], "protocol": "tcp"},
    {"virtual_machine": test_spaces_vm.id, "name": "ssh", "ports": [22], "protocol": "tcp"},
]

created_services = make_nautobot_calls(nb.ipam.services, services)


# Create Circuit Provider
providers = [{"name": "test-provider"}]
created_providers = make_nautobot_calls(nb.circuits.providers, providers)
test_provider = nb.circuits.providers.get(name="test-provider")

# Create Provider Networks
provider_networks = [{"name": "test-provider-network", "provider": test_provider.id}]
created_provider_networks = make_nautobot_calls(nb.circuits.provider_networks, provider_networks)

# Create Circuit Type
circuit_types = [{"name": "test-circuit-type"}]
created_circuit_types = make_nautobot_calls(nb.circuits.circuit_types, circuit_types)
test_circuit_type = nb.circuits.circuit_types.get(name="test-circuit-type")

# Create Circuit
circuits = [
    {"cid": "test-circuit", "provider": test_provider.id, "circuit_type": test_circuit_type.id, "status": {"name": "Active"}},
    {"cid": "test-circuit-two", "provider": test_provider.id, "circuit_type": test_circuit_type.id, "status": {"name": "Active"}},
]
created_circuits = make_nautobot_calls(nb.circuits.circuits, circuits)
test_circuit_two = nb.circuits.circuits.get(cid="test-circuit-two")

# Create Circuit Termination
circuit_terms = [{"circuit": test_circuit_two.id, "term_side": "A", "port_speed": 10000, "location": location_parent.id}]
created_circuit_terms = make_nautobot_calls(nb.circuits.circuit_terminations, circuit_terms)

route_targets = [
    {"name": "4000:4000"},
    {"name": "5000:5000"},
    {"name": "6000:6000"},
]
created_route_targets = make_nautobot_calls(nb.ipam.route_targets, route_targets)

# Create Relationship
relationships = [
    {
        "label": "VLAN to Device",
        "key": "vlan_to_device",
        "type": "one-to-one",
        "source_type": "ipam.vlan",
        "destination_type": "dcim.device",
    },
]
created_relationships = make_nautobot_calls(nb.extras.relationships, relationships)

if ERRORS:
    sys.exit("Errors have occurred when creating objects, and should have been printed out. Check previous output.")
