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
nb_version = version.parse(nb.version)

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
        {"name": "First", "slug": "first"},
        {"name": "Second", "slug": "second"},
        {"name": "Third", "slug": "third"},
        {"name": "Schnozzberry", "slug": "schnozzberry"},
        {"name": "Lookup", "slug": "lookup"},
        {"name": "Nolookup", "slug": "nolookup"},
        {"name": "tagA", "slug": "taga"},
        {"name": "tagB", "slug": "tagb"},
        {"name": "tagC", "slug": "tagc"},
        {"name": "Updated", "slug": "updated"},
    ],
)

# ORDER OF OPERATIONS FOR THE MOST PART

## Create TENANTS
tenants = [{"name": "Test Tenant", "slug": "test-tenant"}]
created_tenants = make_nautobot_calls(nb.tenancy.tenants, tenants)
### Test Tenant to be used later on
test_tenant = nb.tenancy.tenants.get(slug="test-tenant")


## Create TENANT GROUPS
tenant_groups = [{"name": "Test Tenant Group", "slug": "test-tenant-group"}]
created_tenant_groups = make_nautobot_calls(nb.tenancy.tenant_groups, tenant_groups)


## Create Regions
regions = [
    {"name": "Test Region", "slug": "test-region"},
    {"name": "Parent Region", "slug": "parent-region"},
    {"name": "Other Region", "slug": "other-region"},
]
created_regions = make_nautobot_calls(nb.dcim.regions, regions)
### Region variables to be used later on
parent_region = nb.dcim.regions.get(slug="parent-region")
test_region = nb.dcim.regions.get(slug="test-region")

### Create relationship between regions
test_region.parent = parent_region
test_region.save()


## Create SITES and register variables
sites = [
    {
        "name": "Test Site",
        "slug": "test-site",
        "tenant": test_tenant.id,
        "region": test_region.id,
        "status": "active",
    },
    {"name": "Test Site2", "slug": "test-site2", "status": "active"},
]
created_sites = make_nautobot_calls(nb.dcim.sites, sites)
### Site variables to be used later on
test_site = nb.dcim.sites.get(slug="test-site")
test_site2 = nb.dcim.sites.get(slug="test-site2")

### Create power panel
power_panels = [{"name": "Test Power Panel", "site": test_site.id}]
created_power_panels = make_nautobot_calls(nb.dcim.power_panels, power_panels)

## Create VRFs
vrfs = [{"name": "Test VRF", "rd": "1:1"}]
created_vrfs = make_nautobot_calls(nb.ipam.vrfs, vrfs)


## Create PREFIXES
prefixes = [
    {"prefix": "192.168.100.0/24", "site": test_site2.id, "status": "active"},
    {"prefix": "10.10.0.0/16", "status": "active"},
]
created_prefixes = make_nautobot_calls(nb.ipam.prefixes, prefixes)


## Create VLAN GROUPS
vlan_groups = [
    {
        "name": "Test Vlan Group",
        "slug": "test-vlan-group",
        "site": test_site.id,
        "tenant": test_tenant.id,
    },
    {
        "name": "Test Vlan Group 2",
        "slug": "test-vlan-group-2",
        "site": test_site.id,
        "tenant": test_tenant.id,
    },
]
created_vlan_groups = make_nautobot_calls(nb.ipam.vlan_groups, vlan_groups)
## VLAN Group variables to be used later on
test_vlan_group = nb.ipam.vlan_groups.get(slug="test-vlan-group")


## Create VLANS
vlans = [
    {"name": "Wireless", "vid": 100, "site": test_site.id, "status": "active"},
    {"name": "Data", "vid": 200, "site": test_site.id, "status": "active"},
    {"name": "VoIP", "vid": 300, "site": test_site.id, "status": "active"},
    {
        "name": "Test VLAN",
        "vid": 400,
        "site": test_site.id,
        "tenant": test_tenant.id,
        "group": test_vlan_group.id,
        "status": "active",
    },
]
created_vlans = make_nautobot_calls(nb.ipam.vlans, vlans)


## Create IPAM Roles
ipam_roles = [{"name": "Network of care", "slug": "network-of-care"}]
create_ipam_roles = make_nautobot_calls(nb.ipam.roles, ipam_roles)


## Create Manufacturers
manufacturers = [
    {"name": "Cisco", "slug": "cisco"},
    {"name": "Arista", "slug": "arista"},
    {"name": "Test Manufactuer", "slug": "test-manufacturer"},
]
created_manufacturers = make_nautobot_calls(nb.dcim.manufacturers, manufacturers)
### Manufacturer variables to be used later on
cisco_manu = nb.dcim.manufacturers.get(slug="cisco")
arista_manu = nb.dcim.manufacturers.get(slug="arista")


## Create Device Types
device_types = [
    {"model": "Cisco Test", "slug": "cisco-test", "manufacturer": cisco_manu.id},
    {"model": "Arista Test", "slug": "arista-test", "manufacturer": arista_manu.id},
    {
        "model": "Nexus Parent",
        "slug": "nexus-parent",
        "u_height": 0,
        "manufacturer": cisco_manu.id,
        "subdevice_role": "parent",
    },
    {
        "model": "Nexus Child",
        "slug": "nexus-child",
        "u_height": 0,
        "manufacturer": cisco_manu.id,
        "subdevice_role": "child",
    },
    {"model": "1841", "slug": "1841", "manufacturer": cisco_manu.id,},
]

created_device_types = make_nautobot_calls(nb.dcim.device_types, device_types)
### Device type variables to be used later on
cisco_test = nb.dcim.device_types.get(slug="cisco-test")
arista_test = nb.dcim.device_types.get(slug="arista-test")
nexus_parent = nb.dcim.device_types.get(slug="nexus-parent")
nexus_child = nb.dcim.device_types.get(slug="nexus-child")

# Create Rear Port Template
rear_port_templates = [
    {
        "name": "Test Rear Port Template",
        "device_type": cisco_test.id,
        "type": "bnc",
        "positions": 5,
    }
]
created_rear_port_templates = make_nautobot_calls(
    nb.dcim.rear_port_templates, rear_port_templates
)

## Create Device Roles
device_roles = [
    {"name": "Core Switch", "slug": "core-switch", "color": "aa1409", "vm_role": False},
    {
        "name": "Test VM Role",
        "slug": "test-vm-role",
        "color": "e91e63",
        "vm_role": True,
    },
    {
        "name": "Test VM Role 1",
        "slug": "test-vm-role-1",
        "color": "e91e65",
        "vm_role": True,
    },
]
created_device_roles = make_nautobot_calls(nb.dcim.device_roles, device_roles)
### Device role variables to be used later on
core_switch = nb.dcim.device_roles.get(slug="core-switch")


## Create Rack Groups
rack_groups = [
    {"name": "Test Rack Group", "slug": "test-rack-group", "site": test_site.id},
    {"name": "Parent Rack Group", "slug": "parent-rack-group", "site": test_site.id},
]
created_rack_groups = make_nautobot_calls(nb.dcim.rack_groups, rack_groups)

rack_group1 = nb.dcim.rack_groups.get(slug="test-rack-group")
rack_group2 = nb.dcim.rack_groups.get(slug="parent-rack-group")
### Create Rack Group Parent relationship
rack_group1.parent = rack_group2.id
rack_group1.save()

## Create Rack Roles
rack_roles = [{"name": "Test Rack Role", "slug": "test-rack-role", "color": "4287f5"}]
created_rack_roles = make_nautobot_calls(nb.dcim.rack_roles, rack_roles)
rack_role1 = nb.dcim.rack_roles.get(slug="test-rack-role")

## Create Racks
racks = [
    {
        "name": "Test Rack Site 2",
        "site": test_site2.id,
        "role": rack_role1.id,
        "status": "active",
    },
    {
        "name": "Test Rack",
        "site": test_site.id,
        "group": rack_group1.id,
        "status": "active",
    },
]
created_racks = make_nautobot_calls(nb.dcim.racks, racks)
test_rack = nb.dcim.racks.get(name="Test Rack")  # racks don't have slugs
test_rack_site2 = nb.dcim.racks.get(name="Test Rack Site 2")


## Create Devices
devices = [
    {
        "name": "test100",
        "device_type": cisco_test.id,
        "device_role": core_switch.id,
        "site": test_site.id,
        "local_context_data": {"ntp_servers": ["pool.ntp.org"]},
        "status": "active",
    },
    {
        "name": "TestDeviceR1",
        "device_type": cisco_test.id,
        "device_role": core_switch.id,
        "site": test_site.id,
        "rack": test_rack.id,
        "status": "active",
    },
    {
        "name": "R1-Device",
        "device_type": cisco_test.id,
        "device_role": core_switch.id,
        "site": test_site2.id,
        "rack": test_rack_site2.id,
        "status": "active",
    },
    {
        "name": "Test Nexus One",
        "device_type": nexus_parent.id,
        "device_role": core_switch.id,
        "site": test_site.id,
        "status": "active",
    },
    {
        "name": "Test Nexus Child One",
        "device_type": nexus_child.id,
        "device_role": core_switch.id,
        "site": test_site.id,
        "status": "active",
    },
]
created_devices = make_nautobot_calls(nb.dcim.devices, devices)
### Device variables to be used later on
test100 = nb.dcim.devices.get(name="test100")

### Create rear port
rear_ports = [
    {"name": "Test Rear Port", "device": test100.id, "type": "bnc", "positions": 5}
]
created_rear_ports = make_nautobot_calls(nb.dcim.rear_ports, rear_ports)

### Create power ports
power_ports = [{"name": "Test Power Port", "device": test100.id}]
created_power_ports = make_nautobot_calls(nb.dcim.power_ports, power_ports)

### Create console ports
console_ports = [{"name": "Test Console Port", "device": test100.id}]
created_console_ports = make_nautobot_calls(nb.dcim.console_ports, console_ports)

### Create console server ports
console_server_ports = [{"name": "Test Console Server Port", "device": test100.id}]
created_console_server_ports = make_nautobot_calls(
    nb.dcim.console_server_ports, console_server_ports
)

# Create VC, assign member, create initial interface
nexus = nb.dcim.devices.get(name="Test Nexus One")
created_vcs = make_nautobot_calls(
    nb.dcim.virtual_chassis, {"name": "VC1", "master": nexus.id}
)
vc = nb.dcim.virtual_chassis.get(name="VC1")
nexus_child = nb.dcim.devices.get(name="Test Nexus Child One")
nexus_child.update({"virtual_chassis": vc.id, "vc_position": 2})
nexus.update({"vc_position": 0})
nexus_interfaces = [
    {"device": nexus.id, "name": "Ethernet1/1", "type": "1000base-t"},
    {"device": nexus_child.id, "name": "Ethernet2/1", "type": "1000base-t"},
]
created_nexus_interfaces = make_nautobot_calls(nb.dcim.interfaces, nexus_interfaces)

## Create Interfaces
dev_interfaces = [
    {"name": "GigabitEthernet1", "device": test100.id, "type": "1000base-t"},
    {"name": "GigabitEthernet2", "device": test100.id, "type": "1000base-t"},
]
created_interfaces = make_nautobot_calls(nb.dcim.interfaces, dev_interfaces)
nexus_eth1 = nb.dcim.interfaces.get(device_id=nexus.id, name="Ethernet1/1")
nexus_child_eth1 = nb.dcim.interfaces.get(device_id=nexus_child.id, name="Ethernet2/1")

## Interface variables to be used later on
test100_gi1 = nb.dcim.interfaces.get(name="GigabitEthernet1", device_id=test100.id)
test100_gi2 = nb.dcim.interfaces.get(name="GigabitEthernet2", device_id=test100.id)


## Create IP Addresses
ip_addresses = [
    {
        "address": "172.16.180.1/24",
        "assigned_object_type": "dcim.interface",
        "assigned_object_id": test100_gi1.id,
        "status": "active",
    },
    {
        "address": "2001::1:1/64",
        "assigned_object_type": "dcim.interface",
        "assigned_object_id": test100_gi2.id,
        "status": "active",
    },
    {
        "address": "172.16.180.11/24",
        "assigned_object_type": "dcim.interface",
        "assigned_object_id": nexus_eth1.id,
        "status": "active",
    },
    {
        "address": "172.16.180.12/24",
        "assigned_object_type": "dcim.interface",
        "assigned_object_id": nexus_child_eth1.id,
        "dns_name": "nexus.example.com",
        "status": "active",
    },
    {"address": "172.16.180.254/24", "status": "active"},
]

created_ip_addresses = make_nautobot_calls(nb.ipam.ip_addresses, ip_addresses)
# Grab first two IPs
ip1 = nb.ipam.ip_addresses.get(
    address="172.16.180.1/24", assigned_object_id=test100_gi1.id
)
ip2 = nb.ipam.ip_addresses.get(
    address="2001::1:1/64", assigned_object_id=test100_gi2.id
)

# Assign Primary IP
nexus_eth1_ip = nb.ipam.ip_addresses.get(
    address="172.16.180.11/24", assigned_object_id=nexus_eth1.id
)
nexus.update({"primary_ip4": nexus_eth1_ip})

## Create RIRs
rirs = [{"name": "Example RIR", "slug": "example-rir"}]
created_rirs = make_nautobot_calls(nb.ipam.rirs, rirs)

## Create Cluster Group
cluster_groups = [{"name": "Test Cluster Group", "slug": "test-cluster-group"}]
created_cluster_groups = make_nautobot_calls(
    nb.virtualization.cluster_groups, cluster_groups
)
test_cluster_group = nb.virtualization.cluster_groups.get(slug="test-cluster-group")

## Create Cluster Type
cluster_types = [{"name": "Test Cluster Type", "slug": "test-cluster-type"}]
created_cluster_types = make_nautobot_calls(
    nb.virtualization.cluster_types, cluster_types
)
test_cluster_type = nb.virtualization.cluster_types.get(slug="test-cluster-type")

## Create Cluster
clusters = [
    {
        "name": "Test Cluster",
        "type": test_cluster_type.id,
        "group": test_cluster_group.id,
        "site": test_site.id,
    },
    {"name": "Test Cluster 2", "type": test_cluster_type.id},
]
created_clusters = make_nautobot_calls(nb.virtualization.clusters, clusters)
test_cluster = nb.virtualization.clusters.get(name="Test Cluster")
test_cluster2 = nb.virtualization.clusters.get(name="Test Cluster 2")

## Create Virtual Machine
virtual_machines = [
    {"name": "test100-vm", "cluster": test_cluster.id, "status": "active"},
    {"name": "test101-vm", "cluster": test_cluster.id, "status": "active"},
    {"name": "test102-vm", "cluster": test_cluster.id, "status": "active"},
    {"name": "test103-vm", "cluster": test_cluster.id, "status": "active"},
    {"name": "test104-vm", "cluster": test_cluster2.id, "status": "active"},
    {"name": "Test VM With Spaces", "cluster": test_cluster2.id, "status": "active",},
]
created_virtual_machines = make_nautobot_calls(
    nb.virtualization.virtual_machines, virtual_machines
)
test100_vm = nb.virtualization.virtual_machines.get(name="test100-vm")
test101_vm = nb.virtualization.virtual_machines.get(name="test101-vm")
test_spaces_vm = nb.virtualization.virtual_machines.get(name="Test VM With Spaces")

## Create Virtual Machine Interfaces
virtual_machines_intfs = [
    # Create test100-vm intfs
    {"name": "Eth0", "virtual_machine": test100_vm.id},
    {"name": "Eth1", "virtual_machine": test100_vm.id},
    {"name": "Eth2", "virtual_machine": test100_vm.id},
    {"name": "Eth3", "virtual_machine": test100_vm.id},
    {"name": "Eth4", "virtual_machine": test100_vm.id},
    # Create test101-vm intfs
    {"name": "Eth0", "virtual_machine": test101_vm.id},
    {"name": "Eth1", "virtual_machine": test101_vm.id},
    {"name": "Eth2", "virtual_machine": test101_vm.id},
    {"name": "Eth3", "virtual_machine": test101_vm.id},
    {"name": "Eth4", "virtual_machine": test101_vm.id},
    # Create Test VM With Spaces intfs
    {"name": "Eth0", "virtual_machine": test_spaces_vm.id},
    {"name": "Eth1", "virtual_machine": test_spaces_vm.id},
]
created_virtual_machines_intfs = make_nautobot_calls(
    nb.virtualization.interfaces, virtual_machines_intfs
)


## Create Services
services = [
    {"device": test100.id, "name": "ssh", "ports": [22], "protocol": "tcp"},
    {
        "device": test100.id,
        "name": "http",
        "ports": [80],
        "protocol": "tcp",
        "ipaddresses": [ip1.id, ip2.id],
    },
    {"device": nexus.id, "name": "telnet", "ports": [23], "protocol": "tcp"},
    {
        "virtual_machine": test_spaces_vm.id,
        "name": "ssh",
        "ports": [22],
        "protocol": "tcp",
    },
]

created_services = make_nautobot_calls(nb.ipam.services, services)


## Create Circuit Provider
providers = [{"name": "Test Provider", "slug": "test-provider"}]
created_providers = make_nautobot_calls(nb.circuits.providers, providers)
test_provider = nb.circuits.providers.get(slug="test-provider")

## Create Circuit Type
circuit_types = [{"name": "Test Circuit Type", "slug": "test-circuit-type"}]
created_circuit_types = make_nautobot_calls(nb.circuits.circuit_types, circuit_types)
test_circuit_type = nb.circuits.circuit_types.get(slug="test-circuit-type")

## Create Circuit
circuits = [
    {
        "cid": "Test Circuit",
        "provider": test_provider.id,
        "type": test_circuit_type.id,
        "status": "active",
    },
    {
        "cid": "Test Circuit Two",
        "provider": test_provider.id,
        "type": test_circuit_type.id,
        "status": "active",
    },
]
created_circuits = make_nautobot_calls(nb.circuits.circuits, circuits)
test_circuit_two = nb.circuits.circuits.get(cid="Test Circuit Two")

## Create Circuit Termination
circuit_terms = [
    {
        "circuit": test_circuit_two.id,
        "term_side": "A",
        "port_speed": 10000,
        "site": test_site.id,
    }
]
created_circuit_terms = make_nautobot_calls(
    nb.circuits.circuit_terminations, circuit_terms
)

route_targets = [
    {"name": "4000:4000"},
    {"name": "5000:5000"},
    {"name": "6000:6000"},
]
created_route_targets = make_nautobot_calls(nb.ipam.route_targets, route_targets)

if ERRORS:
    sys.exit(
        "Errors have occurred when creating objects, and should have been printed out. Check previous output."
    )
