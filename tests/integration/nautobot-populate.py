#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys
import pynautobot
from packaging import version

# Set nb variable to connect to Nautobot and use the variable in future calls
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
        print(f"Error creating endpoint {endpoint} with payload {payload}: {e.error}")
        global ERRORS  # pylint: disable=global-statement
        ERRORS = True
        return

    return created


# Create tags used in future tests
tags = [
    {"name": "First", "content_types": ["dcim.device", "ipam.routetarget"]},
    {"name": "Second", "content_types": ["dcim.device", "ipam.routetarget"]},
    {"name": "Third", "content_types": ["dcim.device"]},
    {
        "name": "Schnozzberry",
        "content_types": [
            "dcim.device",
            "dcim.rack",
            "ipam.ipaddress",
            "ipam.prefix",
            "ipam.service",
            "ipam.vlan",
            "ipam.vrf",
            "dcim.devicebay",
            "dcim.inventoryitem",
            "virtualization.virtualmachine",
            "virtualization.cluster",
            "virtualization.vminterface",
        ],
    },
    {"name": "Lookup", "content_types": ["dcim.device"]},
    {"name": "Nolookup", "content_types": ["dcim.device"]},
    {"name": "tagA", "content_types": ["dcim.device", "tenancy.tenant"]},
    {"name": "tagB", "content_types": ["dcim.device", "tenancy.tenant"]},
    {"name": "tagC", "content_types": ["dcim.device", "tenancy.tenant"]},
    {"name": "Updated", "content_types": ["dcim.device", "ipam.ipaddress"]},
]

if nautobot_version >= version.parse("2.2"):
    tags.append({"name": "Controller Tag", "content_types": ["dcim.controller"]})
if nautobot_version >= version.parse("2.3"):
    tags.append({"name": "Dynamic Group Tag", "content_types": ["extras.dynamicgroup"]})

create_tags = make_nautobot_calls(nb.extras.tags, tags)


# ORDER OF OPERATIONS FOR THE MOST PART
# Create Admin Users
admin_users = [{"username": "a_admin_user", "is_staff": True, "is_superuser": True}]
created_admin_users = make_nautobot_calls(nb.users.users, admin_users)

# Create Admin User Groups
admin_groups = [
    {"name": "A Test Admin User Group"},
    {"name": "A Test Admin User Group 2"},
    {"name": "A Test Admin User Group 3"},
]
created_admin_groups = make_nautobot_calls(nb.users.groups, admin_groups)

# Create TENANT GROUPS
tenant_groups = [{"name": "Test Tenant Group"}]
created_tenant_groups = make_nautobot_calls(nb.tenancy.tenant_groups, tenant_groups)
test_tenant_group = nb.tenancy.tenant_groups.get(name="Test Tenant Group")

# Create TENANTS
tenants = [{"name": "Test Tenant", "tenant_group": test_tenant_group.id}]
created_tenants = make_nautobot_calls(nb.tenancy.tenants, tenants)
# Test Tenant to be used later on
test_tenant = nb.tenancy.tenants.get(name="Test Tenant")

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

if nautobot_version >= version.parse("2.2"):
    location_content_types.append("dcim.controller")
if nautobot_version >= version.parse("2.3"):
    location_content_types.append("dcim.module")

location_types = [{"name": "My Parent Location Type", "content_types": location_content_types, "nestable": True}]
created_location_types = make_nautobot_calls(nb.dcim.location_types, location_types)
parent_location_type = nb.dcim.location_types.get(name="My Parent Location Type")

# Create child location types
child_location_types = [
    {
        "name": "My Child Location Type",
        "content_types": location_content_types,
        "nestable": True,
        "parent": parent_location_type.id,
    }
]
created_child_location_types = make_nautobot_calls(nb.dcim.location_types, child_location_types)
child_location_type = nb.dcim.location_types.get(name="My Child Location Type")

# Create locations
parent_location_attrs = [
    {"name": "Parent Test Location", "location_type": parent_location_type.id, "tenant": test_tenant.id, "status": {"name": "Active"}},
    {"name": "Parent Test Location 2", "location_type": parent_location_type.id, "tenant": test_tenant.id, "status": {"name": "Active"}},
    {"name": "Prefix Test Location", "location_type": parent_location_type.id, "tenant": test_tenant.id, "status": {"name": "Active"}},
]
make_nautobot_calls(nb.dcim.locations, parent_location_attrs)

# Location variables to be used later on
location_parent = nb.dcim.locations.get(name="Parent Test Location")
location_parent2 = nb.dcim.locations.get(name="Parent Test Location 2")
child_location_attrs = [
    {"name": "Child Test Location", "location_type": child_location_type.id, "parent": location_parent.id, "status": {"name": "Active"}},
    # Creating an intentionally duplicate location name with different parent to test looking up by parent
    {"name": "Child Test Location", "location_type": child_location_type.id, "parent": location_parent2.id, "status": {"name": "Active"}},
]
make_nautobot_calls(nb.dcim.locations, child_location_attrs)
location_child = nb.dcim.locations.get(name="Child Test Location", parent="Parent Test Location")

child_child_location_attrs = [
    {"name": "Child-Child Test Location", "location_type": child_location_type.id, "parent": location_child.id, "status": {"name": "Active"}},
]
make_nautobot_calls(nb.dcim.locations, child_child_location_attrs)
location_child_child = nb.dcim.locations.get(name="Child-Child Test Location")
# Create power panel
power_panels = [{"name": "Test Power Panel", "location": location_parent.id}]
created_power_panels = make_nautobot_calls(nb.dcim.power_panels, power_panels)

# Create VRFs
vrfs = [{"name": "Test VRF", "rd": "1:1", "namespace": {"name": "Global"}}]
created_vrfs = make_nautobot_calls(nb.ipam.vrfs, vrfs)

# Create namespace
namespaces = [{"name": "Private"}]
created_namespaces = make_nautobot_calls(nb.ipam.namespaces, namespaces)

# Create PREFIXES
prefixes = [
    {"prefix": "192.168.0.0/16", "location": location_parent.id, "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "10.0.0.0/8", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "10.10.0.0/16", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "172.16.0.0/12", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "172.16.0.0/12", "status": {"name": "Active"}, "namespace": {"name": "Private"}},
    {"prefix": "192.0.2.0/24", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
    {"prefix": "2001::1:0/64", "status": {"name": "Active"}, "namespace": {"name": "Global"}},
]
created_prefixes = make_nautobot_calls(nb.ipam.prefixes, prefixes)


# Create VLAN GROUPS
vlan_groups = [
    {"name": "Test Vlan Group", "location": location_child.id, "tenant": test_tenant.id},
    {"name": "Test Vlan Group 2", "location": location_child.id, "tenant": test_tenant.id},
]
created_vlan_groups = make_nautobot_calls(nb.ipam.vlan_groups, vlan_groups)
# VLAN Group variables to be used later on
test_vlan_group = nb.ipam.vlan_groups.get(name="Test Vlan Group")


# Create VLANS
vlans = [
    {"name": "Wireless", "vid": 100, "location": location_child.id, "status": {"name": "Active"}},
    {"name": "Data", "vid": 200, "location": location_child.id, "status": {"name": "Active"}},
    {"name": "VoIP", "vid": 300, "location": location_child.id, "status": {"name": "Active"}},
    {
        "name": "Test VLAN",
        "vid": 400,
        "location": location_child.id,
        "tenant": test_tenant.id,
        "vlan_group": test_vlan_group.id,
        "status": {"name": "Active"},
    },
    {"name": "Test VLAN 600", "vid": 600, "status": {"name": "Active"}},
]
created_vlans = make_nautobot_calls(nb.ipam.vlans, vlans)


# Create IPAM Roles
ipam_roles = [{"name": "Network of care", "content_types": ["ipam.prefix", "ipam.vlan"]}]
create_ipam_roles = make_nautobot_calls(nb.extras.roles, ipam_roles)


# Create Manufacturers
manufacturers = [
    {"name": "Cisco"},
    {"name": "Arista"},
    {"name": "Test Manufacturer"},
]
created_manufacturers = make_nautobot_calls(nb.dcim.manufacturers, manufacturers)
# Manufacturer variables to be used later on
cisco_manu = nb.dcim.manufacturers.get(name="Cisco")
arista_manu = nb.dcim.manufacturers.get(name="Arista")

# Create Platforms
platforms = [{"name": "Cisco IOS", "manufacturer": cisco_manu.id, "network_driver": "cisco_ios", "napalm_driver": "ios"}]
created_platforms = make_nautobot_calls(nb.dcim.platforms, platforms)

# Create Device Types
device_types = [
    {"model": "Cisco Test", "manufacturer": cisco_manu.id},
    {"model": "Cisco Test 2", "manufacturer": cisco_manu.id},
    {"model": "Arista Test", "manufacturer": arista_manu.id},
    {
        "model": "Nexus Parent",
        "u_height": 0,
        "manufacturer": cisco_manu.id,
        "subdevice_role": "parent",
    },
    {
        "model": "Nexus Child",
        "u_height": 0,
        "manufacturer": cisco_manu.id,
        "subdevice_role": "child",
    },
    {"model": "1841", "manufacturer": cisco_manu.id},
]

created_device_types = make_nautobot_calls(nb.dcim.device_types, device_types)
# Device type variables to be used later on
cisco_test = nb.dcim.device_types.get(model="Cisco Test")
arista_test = nb.dcim.device_types.get(model="Arista Test")
nexus_parent = nb.dcim.device_types.get(model="Nexus Parent")
nexus_child = nb.dcim.device_types.get(model="Nexus Child")

# Create Rear Port Template
rear_port_templates = [{"name": "Test Rear Port Template", "device_type": cisco_test.id, "type": "bnc", "positions": 5}]
created_rear_port_templates = make_nautobot_calls(nb.dcim.rear_port_templates, rear_port_templates)

# Create Device Roles
device_roles = [
    {"name": "Core Switch", "color": "aa1409", "vm_role": False, "content_types": ["dcim.device"]},
    {"name": "Test VM Role", "color": "e91e63", "vm_role": True, "content_types": ["virtualization.virtualmachine"]},
    {"name": "Test VM Role 1", "color": "e91e65", "vm_role": True, "content_types": ["dcim.device", "virtualization.virtualmachine"]},
]

if nautobot_version >= version.parse("2.2"):
    device_roles.append({"name": "Test Controller Role", "color": "e91e65", "vm_role": False, "content_types": ["dcim.controller"]})
if nautobot_version >= version.parse("2.3"):
    device_roles.append({"name": "Test Module Role", "color": "795548", "vm_role": False, "content_types": ["dcim.module"]})

created_device_roles = make_nautobot_calls(nb.extras.roles, device_roles)

# Device role variables to be used later on
core_switch = nb.extras.roles.get(name="Core Switch")

# Create Rack Groups
rack_groups = [
    {"name": "Parent Rack Group", "location": location_child.id},
    {"name": "Child Rack Group", "location": location_child_child.id},
]
created_rack_groups = make_nautobot_calls(nb.dcim.rack_groups, rack_groups)

rack_group_parent = nb.dcim.rack_groups.get(name="Parent Rack Group")
rack_group_child = nb.dcim.rack_groups.get(name="Child Rack Group")
# Create Rack Group Parent relationship
rack_group_child.parent = rack_group_parent.id
rack_group_child.save()

# Create Rack Roles
rack_roles = [{"name": "Test Rack Role", "color": "4287f5", "content_types": ["dcim.rack"]}]
created_rack_roles = make_nautobot_calls(nb.extras.roles, rack_roles)
rack_role1 = nb.extras.roles.get(name="Test Rack Role")

# Create Racks
racks = [
    {"name": "Sub Test Rack", "location": location_child_child.id, "rack_group": rack_group_child.id, "status": {"name": "Active"}},
    {"name": "Main Test Rack", "location": location_child.id, "rack_group": rack_group_parent.id, "role": rack_role1.id, "status": {"name": "Active"}},
]
created_racks = make_nautobot_calls(nb.dcim.racks, racks)
main_test_rack = nb.dcim.racks.get(name="Main Test Rack")
sub_test_rack = nb.dcim.racks.get(name="Sub Test Rack")


# Create Devices
devices = [
    {
        "name": "test100",
        "device_type": cisco_test.id,
        "role": core_switch.id,
        "location": location_child.id,
        "tenant": test_tenant.id,
        "local_config_context_data": {"ntp_servers": ["pool.ntp.org"]},
        "status": {"name": "Active"},
    },
    {
        "name": "TestDeviceR1",
        "device_type": cisco_test.id,
        "role": core_switch.id,
        "location": location_child_child.id,
        "rack": sub_test_rack.id,
        "status": {"name": "Active"},
    },
    {
        "name": "R1-Device",
        "device_type": cisco_test.id,
        "role": core_switch.id,
        "location": location_child.id,
        "rack": main_test_rack.id,
        "status": {"name": "Active"},
    },
    {
        "name": "Test Nexus One",
        "device_type": nexus_parent.id,
        "role": core_switch.id,
        "location": location_child.id,
        "status": {"name": "Active"},
    },
    {
        "name": "Test Nexus Child One",
        "device_type": nexus_child.id,
        "role": core_switch.id,
        "location": location_child.id,
        "status": {"name": "Active"},
    },
]
created_devices = make_nautobot_calls(nb.dcim.devices, devices)
# Device variables to be used later on
test100 = nb.dcim.devices.get(name="test100")
test_device_r1 = nb.dcim.devices.get(name="TestDeviceR1")

# Create rear port
rear_ports = [{"name": "Test Rear Port", "device": test100.id, "type": "bnc", "positions": 5}]
created_rear_ports = make_nautobot_calls(nb.dcim.rear_ports, rear_ports)

# Create power ports
power_ports = [{"name": "Test Power Port", "device": test100.id}]
created_power_ports = make_nautobot_calls(nb.dcim.power_ports, power_ports)

# Create power outlets
power_outlets = [{"name": "R1 Power Outlet", "device": test_device_r1.id}]
created_power_outlets = make_nautobot_calls(nb.dcim.power_outlets, power_outlets)

# Create console ports
console_ports = [{"name": "Test Console Port", "device": test100.id}]
created_console_ports = make_nautobot_calls(nb.dcim.console_ports, console_ports)

# Create console server ports
console_server_ports = [{"name": "Test Console Server Port", "device": test100.id}]
created_console_server_ports = make_nautobot_calls(nb.dcim.console_server_ports, console_server_ports)

# Create VC, assign member, create initial interface
nexus = nb.dcim.devices.get(name="Test Nexus One")
created_vcs = make_nautobot_calls(nb.dcim.virtual_chassis, {"name": "VC1", "master": nexus.id})
vc = nb.dcim.virtual_chassis.get(name="VC1")
nexus_child = nb.dcim.devices.get(name="Test Nexus Child One")
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
    {"name": "GigabitEthernet3", "device": test100.id, "type": "1000base-t", "status": {"name": "Active"}},
    {"name": "GigabitEthernet4", "device": test100.id, "type": "1000base-t", "status": {"name": "Active"}},
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
        "namespace": {"name": "Global"},
        "status": {"name": "Active"},
    },
    {
        "address": "2001::1:1/64",
        "namespace": {"name": "Global"},
        "status": {"name": "Active"},
    },
    {
        "address": "172.16.180.11/24",
        "dns_name": "nexus.example.com",
        "namespace": {"name": "Global"},
        "status": {"name": "Active"},
    },
    {
        "address": "172.16.180.12/24",
        "namespace": {"name": "Global"},
        "dns_name": "nexus.example.com",
        "status": {"name": "Active"},
    },
    {"address": "172.16.180.254/24", "namespace": {"name": "Global"}, "status": {"name": "Active"}},
    {"address": "10.100.0.1/32", "namespace": {"name": "Global"}, "status": {"name": "Active"}},
    {"address": "10.100.10.1/32", "namespace": {"name": "Global"}, "status": {"name": "Active"}},
]

created_ip_addresses = make_nautobot_calls(nb.ipam.ip_addresses, ip_addresses)
# Grab IPs
ip1 = nb.ipam.ip_addresses.get(address="172.16.180.1/24")
ip2 = nb.ipam.ip_addresses.get(address="2001::1:1/64")
ip3 = nb.ipam.ip_addresses.get(address="172.16.180.11/24")
ip4 = nb.ipam.ip_addresses.get(address="172.16.180.12/24")

# Assign IP to interfaces
ip_to_intf = [
    {
        "ip_address": ip1.id,
        "interface": test100_gi1.id,
    },
    {
        "ip_address": ip2.id,
        "interface": test100_gi2.id,
    },
    {
        "ip_address": ip3.id,
        "interface": nexus_eth1.id,
    },
    {
        "ip_address": ip4.id,
        "interface": nexus_child_eth1.id,
    },
]
created_ip_to_intf = make_nautobot_calls(nb.ipam.ip_address_to_interface, ip_to_intf)

# Assign Primary IP
nexus_eth1_ip = nb.ipam.ip_addresses.get(address="172.16.180.11/24", interfaces=[nexus_eth1.id])
nexus.update({"primary_ip4": nexus_eth1_ip})

# Create RIRs
rirs = [{"name": "Example RIR"}]
created_rirs = make_nautobot_calls(nb.ipam.rirs, rirs)

# Create Cluster Group
cluster_groups = [{"name": "Test Cluster Group"}]
created_cluster_groups = make_nautobot_calls(nb.virtualization.cluster_groups, cluster_groups)
test_cluster_group = nb.virtualization.cluster_groups.get(name="Test Cluster Group")

# Create Cluster Type
cluster_types = [{"name": "Test Cluster Type"}]
created_cluster_types = make_nautobot_calls(nb.virtualization.cluster_types, cluster_types)
test_cluster_type = nb.virtualization.cluster_types.get(name="Test Cluster Type")

# Create Cluster
clusters = [
    {"name": "Test Cluster", "cluster_type": test_cluster_type.id, "cluster_group": test_cluster_group.id, "location": location_child.id},
    {"name": "Test Cluster 2", "cluster_type": test_cluster_type.id},
]
created_clusters = make_nautobot_calls(nb.virtualization.clusters, clusters)
test_cluster = nb.virtualization.clusters.get(name="Test Cluster")
test_cluster2 = nb.virtualization.clusters.get(name="Test Cluster 2")

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
    {"device": test100.id, "name": "http", "ports": [80], "protocol": "tcp", "ip_addresses": [ip1.id, ip2.id]},
    {"device": nexus.id, "name": "telnet", "ports": [23], "protocol": "tcp"},
    {"virtual_machine": test_spaces_vm.id, "name": "ssh", "ports": [22], "protocol": "tcp"},
]

created_services = make_nautobot_calls(nb.ipam.services, services)


# Create Circuit Provider
providers = [{"name": "Test Provider"}]
created_providers = make_nautobot_calls(nb.circuits.providers, providers)
test_provider = nb.circuits.providers.get(name="Test Provider")

# Create Provider Networks
provider_networks = [{"name": "Test Provider Network", "provider": test_provider.id}]
created_provider_networks = make_nautobot_calls(nb.circuits.provider_networks, provider_networks)

# Create Circuit Type
circuit_types = [{"name": "Test Circuit Type"}]
created_circuit_types = make_nautobot_calls(nb.circuits.circuit_types, circuit_types)
test_circuit_type = nb.circuits.circuit_types.get(name="Test Circuit Type")

# Create Circuit
circuits = [
    {"cid": "Test Circuit", "provider": test_provider.id, "circuit_type": test_circuit_type.id, "status": {"name": "Active"}},
    {"cid": "Test Circuit Two", "provider": test_provider.id, "circuit_type": test_circuit_type.id, "status": {"name": "Active"}},
]
created_circuits = make_nautobot_calls(nb.circuits.circuits, circuits)
test_circuit_two = nb.circuits.circuits.get(cid="Test Circuit Two")

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

# Create Secrets
secrets = [
    {
        "name": "Test Secret",
        "provider": "environment-variable",
        "parameters": {
            "variable": "TEST_ENV_VAR",
        },
    }
]
created_secrets = make_nautobot_calls(nb.extras.secrets, secrets)
test_secret = nb.extras.secrets.get(name="Test Secret")

secrets_groups = [
    {
        "name": "Test Secrets Group",
        "secrets": [
            {
                "secret": test_secret.id,
                "access_type": "Generic",
                "secret_type": "secret",
            }
        ],
    }
]
created_secrets_groups = make_nautobot_calls(nb.extras.secrets_groups, secrets_groups)

# Create Device Redundancy Groups
device_redundancy_groups = [
    {
        "name": "My Device Redundancy Group",
        "status": "Active",
    }
]
created_device_redundancy_groups = make_nautobot_calls(nb.dcim.device_redundancy_groups, device_redundancy_groups)

# Create Custom Fields
custom_fields = [
    {
        "label": "My Selection Custom Field",
        "key": "my_selection_custom_field",
        "type": "select",
        "content_types": ["circuits.circuit"],
    },
    {
        "label": "My Text Custom Field",
        "key": "my_text_custom_field",
        "type": "text",
        "content_types": ["circuits.circuit"],
    },
    {
        "label": "My Device Custom Field",
        "key": "my_device_custom_field",
        "type": "text",
        "content_types": ["dcim.device"],
    },
    {
        "label": "My Location Custom Field",
        "key": "my_location_custom_field",
        "type": "text",
        "content_types": ["dcim.location"],
    },
]
created_custom_fields = make_nautobot_calls(nb.extras.custom_fields, custom_fields)

# Set a custom field on a device
test100 = nb.dcim.devices.get(name="test100")
test100.custom_fields = {"my_device_custom_field": "Test Device Custom Field Value"}
test100.save()

# Set a custom field on the location for the device
test100_location = nb.dcim.locations.get(id=test100.location.id)
test100_location.custom_fields = {"my_location_custom_field": "Test Location Custom Field Value"}
test100_location.save()

# Enable example job for job tests
example_job_receiver = nb.extras.jobs.get(name="Example Simple Job Button Receiver")
example_job_receiver.enabled = True
example_job_receiver.save()

###############
# v2.2+ items #
###############
if nautobot_version >= version.parse("2.2"):
    # Create Teams
    teams = [{"name": "My Test Team"}]
    created_teams = make_nautobot_calls(nb.extras.teams, teams)

    # Create Contacts
    contacts = [{"name": "My Contact"}, {"name": "My Contact 2"}]
    created_contacts = make_nautobot_calls(nb.extras.contacts, contacts)

    # Create Controller
    controller = [
        {"name": "controller_one", "location": location_child.id, "status": {"name": "Active"}},
        {"name": "controller_two", "location": location_child.id, "status": {"name": "Active"}},
    ]
    created_controller = make_nautobot_calls(nb.dcim.controllers, controller)

    # Create Controller Managed Device Groups
    test_controller_one = nb.dcim.controllers.get(name="controller_one")
    controller_device_group = [{"name": "controller_group_one", "weight": "1000", "controller": test_controller_one.id}]
    created_controller_device_group = make_nautobot_calls(nb.dcim.controller_managed_device_groups, controller_device_group)

###############
# v2.3+ items #
###############
if nautobot_version >= version.parse("2.3"):
    # Create role for virtual machine interfaces
    vm_interface_roles = [
        {"name": "Test VM Interface Role", "color": "aa1409", "vm_role": False, "content_types": ["virtualization.vminterface"]},
    ]
    created_vm_interface_roles = make_nautobot_calls(nb.extras.roles, vm_interface_roles)

    cloud_resource_types = [
        {"name": "CiscoCloudServiceType", "provider": "Cisco", "content_types": ["cloud.cloudservice"]},
        {"name": "CiscoCloudNetworkType", "provider": "Cisco", "content_types": ["cloud.cloudnetwork"]},
    ]
    created_cloud_resource_types = make_nautobot_calls(nb.cloud.cloud_resource_types, cloud_resource_types)

    cloud_accounts = [{"name": "CiscoCloudAccount", "provider": "Cisco", "account_number": "424242"}]
    created_cloud_accounts = make_nautobot_calls(nb.cloud.cloud_accounts, cloud_accounts)

    cloud_services = [{"name": "CiscoCloudService", "cloud_resource_type": "CiscoCloudServiceType", "cloud_account": "CiscoCloudAccount"}]
    created_cloud_services = make_nautobot_calls(nb.cloud.cloud_services, cloud_services)

    cloud_networks = [{"name": "CiscoCloudNetwork", "cloud_resource_type": "CiscoCloudNetworkType", "cloud_account": "CiscoCloudAccount"}]
    created_cloud_networks = make_nautobot_calls(nb.cloud.cloud_networks, cloud_networks)

    # Create module types
    power_outlet_module_types = [
        {"manufacturer": "Cisco", "model": "HooverMaxProModel60"},
        {"manufacturer": "Cisco", "model": "HooverMaxProModel61"},
    ]
    created_power_outlet_module_types = make_nautobot_calls(nb.dcim.module_types, power_outlet_module_types)

    # Create a module bay
    power_outlet_module_bays = [{"parent_device": test100.id, "name": "PowerStrip"}, {"parent_device": test100.id, "name": "PowerStripTwo"}]
    created_power_outlet_module_bays = make_nautobot_calls(nb.dcim.module_bays, power_outlet_module_bays)

    # Assign module type to module bay
    test_module_type = nb.dcim.module_types.get(model="HooverMaxProModel60")
    test_module_bay = nb.dcim.module_bays.get(name="PowerStrip")
    power_outlet_modules = [{"module_type": test_module_type.id, "status": "Active", "parent_module_bay": test_module_bay.id}]
    created_power_outlet_modules = make_nautobot_calls(nb.dcim.modules, power_outlet_modules)

    # Create Module Rear Port Template
    module_rear_port_templates = [{"name": "Test Module Rear Port Template", "module_type": test_module_type.id, "type": "bnc", "positions": 5}]
    created_rear_port_templates = make_nautobot_calls(nb.dcim.rear_port_templates, module_rear_port_templates)

    # Create role for device interfaces
    device_interface_roles = [
        {"name": "Loop the Network", "color": "111111", "vm_role": False, "content_types": ["dcim.interface"]},
    ]
    created_device_interface_roles = make_nautobot_calls(nb.extras.roles, device_interface_roles)

    # Create metadata_type for metadata_choices
    metadata_types = [
        {"name": "TestMetadataType", "data_type": "multi-select", "content_types": ["dcim.device"]},
        {"name": "TestMetadataContactType", "data_type": "contact-or-team", "content_types": ["dcim.device"]},
        {"name": "TestMetadataTextType", "data_type": "text", "content_types": ["dcim.device"]},
    ]
    created_metadata_types = make_nautobot_calls(nb.extras.metadata_types, metadata_types)

    # Create dynamic group of type static assignment
    dynamic_groups = [{"name": "TestStaticAssociations", "content_type": "dcim.device", "group_type": "static"}]
    created_dynamic_groups = make_nautobot_calls(nb.extras.dynamic_groups, dynamic_groups)


if ERRORS:
    sys.exit("Errors have occurred when creating objects, and should have been printed out. Check previous output.")
