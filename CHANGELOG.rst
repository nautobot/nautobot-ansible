====================================
networktocode.nautobot Release Notes
====================================

.. contents:: Topics


v1.0.4
======

Bugfixes
--------

- Added check for UUIDs when checking for isinstance(int) [#22](https://github.com/nautobot/nautobot-ansible/pull/22)
- ip_address - Removed interface option [#23](https://github.com/nautobot/nautobot-ansible/pull/23)

v1.0.3
======

Bugfixes
--------

- Validate if value is already a UUID, return UUID and do not attempt to resolve [#17](https://github.com/nautobot/nautobot-ansible/pull/17)

v1.0.2
======

Bugfixes
--------

- Remove code related to fetching secrets due to secrets not existing in Nautobot.

v1.0.1
======

Release Summary
---------------

Removes dependency on ansible.netcommon and uses builtin ipaddress module

v1.0.0
======

Release Summary
---------------

This is the first official release of an Ansible Collection for Nautobot.
This project is forked from the ``netbox.netbox`` Ansible Collection.

New Plugins
-----------

Lookup
~~~~~~

- networktocode.nautobot.lookup - Queries and returns elements from Nautobot

New Modules
-----------

- networktocode.nautobot.aggregate - Creates or removes aggregates from Nautobot
- networktocode.nautobot.cable - Create, update or delete cables within Nautobot
- networktocode.nautobot.circuit - Create, update or delete circuits within Nautobot
- networktocode.nautobot.circuit_termination - Create, update or delete circuit terminations within Nautobot
- networktocode.nautobot.circuit_type - Create, update or delete circuit types within Nautobot
- networktocode.nautobot.cluster - Create, update or delete clusters within Nautobot
- networktocode.nautobot.cluster_group - Create, update or delete cluster groups within Nautobot
- networktocode.nautobot.cluster_type - Create, update or delete cluster types within Nautobot
- networktocode.nautobot.console_port - Create, update or delete console ports within Nautobot
- networktocode.nautobot.console_port_template - Create, update or delete console port templates within Nautobot
- networktocode.nautobot.console_server_port - Create, update or delete console server ports within Nautobot
- networktocode.nautobot.console_server_port_template - Create, update or delete console server port templates within Nautobot
- networktocode.nautobot.device - Create, update or delete devices within Nautobot
- networktocode.nautobot.device_bay - Create, update or delete device bays within Nautobot
- networktocode.nautobot.device_bay_template - Create, update or delete device bay templates within Nautobot
- networktocode.nautobot.device_interface - Creates or removes interfaces on devices from Nautobot
- networktocode.nautobot.device_interface_template - Creates or removes interfaces on devices from Nautobot
- networktocode.nautobot.device_role - Create, update or delete devices roles within Nautobot
- networktocode.nautobot.device_type - Create, update or delete device types within Nautobot
- networktocode.nautobot.front_port - Create, update or delete front ports within Nautobot
- networktocode.nautobot.front_port_template - Create, update or delete front port templates within Nautobot
- networktocode.nautobot.inventory_item - Creates or removes inventory items from Nautobot
- networktocode.nautobot.ip_address - Creates or removes IP addresses from Nautobot
- networktocode.nautobot.ipam_role - Creates or removes ipam roles from Nautobot
- networktocode.nautobot.manufacturer - Create or delete manufacturers within Nautobot
- networktocode.nautobot.platform - Create or delete platforms within Nautobot
- networktocode.nautobot.power_feed - Create, update or delete power feeds within Nautobot
- networktocode.nautobot.power_outlet - Create, update or delete power outlets within Nautobot
- networktocode.nautobot.power_outlet_template - Create, update or delete power outlet templates within Nautobot
- networktocode.nautobot.power_panel - Create, update or delete power panels within Nautobot
- networktocode.nautobot.power_port - Create, update or delete power ports within Nautobot
- networktocode.nautobot.power_port_template - Create, update or delete power port templates within Nautobot
- networktocode.nautobot.prefix - Creates or removes prefixes from Nautobot
- networktocode.nautobot.provider - Create, update or delete providers within Nautobot
- networktocode.nautobot.rack - Create, update or delete racks within Nautobot
- networktocode.nautobot.rack_group - Create, update or delete racks groups within Nautobot
- networktocode.nautobot.rack_role - Create, update or delete racks roles within Nautobot
- networktocode.nautobot.rear_port - Create, update or delete rear ports within Nautobot
- networktocode.nautobot.rear_port_template - Create, update or delete rear port templates within Nautobot
- networktocode.nautobot.region - Creates or removes regions from Nautobot
- networktocode.nautobot.rir - Create, update or delete RIRs within Nautobot
- networktocode.nautobot.route_target - Creates or removes route targets from Nautobot
- networktocode.nautobot.service - Creates or removes service from Nautobot
- networktocode.nautobot.site - Creates or removes sites from Nautobot
- networktocode.nautobot.status - Creates or removes status from Nautobot
- networktocode.nautobot.tag - Creates or removes tags from Nautobot
- networktocode.nautobot.tenant - Creates or removes tenants from Nautobot
- networktocode.nautobot.tenant_group - Creates or removes tenant groups from Nautobot
- networktocode.nautobot.virtual_chassis - Create, update or delete virtual chassis within Nautobot
- networktocode.nautobot.virtual_machine - Create, update or delete virtual_machines within Nautobot
- networktocode.nautobot.vlan - Create, update or delete vlans within Nautobot
- networktocode.nautobot.vlan_group - Create, update or delete vlans groups within Nautobot
- networktocode.nautobot.vm_interface - Creates or removes interfaces from virtual machines in Nautobot
- networktocode.nautobot.vrf - Create, update or delete vrfs within Nautobot
