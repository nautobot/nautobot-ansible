====================================
networktocode.nautobot Release Notes
====================================

.. contents:: Topics


v5.3.1
======

Minor Changes
-------------
- (#422) Fixed `admin_permission` module to properly convert list of groups to UUIDs

v5.3.0
======

New Modules
-----------

- networktocode.nautobot.vlan_location - Creates or removes Location assignments to VLANs from Nautobot
- networktocode.nautobot.contact - Creates or removes contacts from Nautobot
- networktocode.nautobot.team - Creates or removes teams from Nautobot
- networktocode.nautobot.controller - Creates or removes controllers from Nautobot
- networktocode.nautobot.admin_user - Creates or removes users from Nautobot
- networktocode.nautobot.admin_group - Creates or removes groups from Nautobot
- networktocode.nautobot.admin_permission - Creates or removes permissions from Nautobot

Minor Changes
-------------
- (#352) Added IPv6 support as the default IP version for `gql_inventory` plugin
- (#415) Added `role` option to `vm_interface` module
- (#416) Fixed `location_type` idempotency for `location` module

v5.2.1
======

Minor Changes
-------------
- (#345) Added `NAUTOBOT_VALIDATE_CERTS` environment variable to disable SSL verification
- (#348) Fixed GraphQL Inventory plugin bug when device platform is None

v5.2.0
======

Minor Changes
-------------
- (#310) Fixed `parent` for location_type to convert to UUID for idempotency
- (#319) Added `custom_fields` to `tag`, `vlan_group` and `role` modules
- (#321) Updated documentation and examples for the `lookup` plugin
- (#323) Added constructed features and inventory cache to the `gql_inventory` plugin
- (#335) Fixed custom field idempotency for various modules
- (#336) Added `custom_fields` to the `inventory_item` module
- (#338) Added `num_retries` to the `lookup` plugin
- (#340) Added `label` and `description` to the `device_interface_template` module

v5.1.1
======

Minor Changes
-------------
- (#298) Removes `status` option from being required unless creating a new object for various modules
- (#299) Added example for using the `depth` option in the `lookup` module
- (#304) Fixed the ability to look up `parent_location` by name instead of UUID in the `location` module

v5.1.0
======

Release Summary
---------------

This release adds various new modules and includes some bug fixes and minor changes.

New Modules
-----------

- networktocode.nautobot.device_redundancy_group - Creates or removes device redundancy groups from Nautobot
- networktocode.nautobot.custom_field - Creates or removes custom fields from Nautobot
- networktocode.nautobot.custom_field_choice - Creates or removes custom field choices from Nautobot
- networktocode.nautobot.namespace - Creates or removes namespaces from Nautobot

Minor Changes
-------------

- (#273) Added custom_fields option to the vm_interface module.
- (#275) Added additional options to the location module that were originally on site and region in Nautobot 1.X.
- (#283) Fixed the following lookup plugins to properly use a dash instead of an underscore:
    - `location-types`
    - `provider-networks`
    - `relationship-associations`
- (#287) Adds the ability to use the UUID, name or name and parent (as key/value pairs) for the `location` parameter in various modules.

v5.0.2
======

Minor Changes
-------------

- (#248) Remove choices from various modules, in favor of pynaubot choices() method.
- (#269) Fix SSL verification.

v5.0.1
======

Minor Changes
-------------

- (#257) Fix plugin module.

v5.0.0
======

Release Summary
---------------

This release updates collection code for compatibility code with Nautobot 2.0, where API has breaking changes. 

Breaking Changes / Porting Guide
--------------------------------

- (#234) Updates for Nautobot 2.0 Compatibility

New Modules
-----------

- networktocode.nautobot.ip_address_to_interface - Creates or removes associations between IP and interface.
- networktocode.nautobot.role - Creates or removes a role. Collapsed from several role modules in DCIM and IPAM.

v4.5.0
======

Release Summary
---------------

Fixes error handling in inventory to not erase inventories, minor bug fixes, and introduces Plugin module

Minor Changes
-------------

- (#211) Removes codecov from dev dependencies
- (#217) Fixes and enables testing for Nautobot 1.5
- (#220) Adds status option to device_interface module

Bugfixes
--------

- (#209) Catches HTTPError for `query_graphql` and fails to enable ansible retries
- (#223) Inventory Hosts Empty On Error
- (#228) Fixes graphql inventory grouping by tags

v4.4.0
======

Minor Changes
-------------

- (#203) Adds plugin module
- (#209) Catches HTTPError for GraphQL query and enables Ansible retries
- (#211) Removes codecov from dev dependencies

v4.3.1
======

Bugfixes
--------

- (#196) Virtual Chassis return multiple result at times

v4.3.0
======

Minor Changes
-------------

- (#185) Updated Doc Fragments
- (#187) Updated Tag documentation
- (#191) Added locations and location_type modules

v4.2.0
======

Minor Changes
-------------

- (#171) Add provider_network to circuit_termination module
- (#172) Add description to manufacturer

v4.1.1
======

Release Summary
---------------

Fix incorrect filter parameters

Bugfixes
--------

- (#163) Fix bad filter params due to `STRICT_FILTERING` being enabled in Nautobot 1.4.

v4.1.0
======

Release Summary
---------------

Fix minor bugs and add API versioning to collection.

Minor Changes
-------------

- (#139) - Add API versioning to compatible plugins.

Bugfixes
--------

- (#159) Lookup - Fix `api_filter` to not attempt to convert UUIDs to integers from legacy forked code.

v4.0.1
======

Release Summary
---------------

Fixes GraphQL inventory plugin bugs and RTD builds.

Bugfixes
--------

- (#150) GraphQL inventory plugin - boolean filters are invalid
- (#151) GraphQL inventory plugin - using group_by can crash if there are empty values
- (#154) Fixes antsibull import for RTD builds

v4.0.0
======

Release Summary
---------------

This release refactors the GraphQL inventory plugin to allow fetching virtual machines and a more flexible approach to allow users to use most of GraphQL's native capabilities.

Breaking Changes / Porting Guide
--------------------------------

- (#130) Refactors GraphQL Inventory plugin to allow custom GraphQL queries with nested levels. Allows virtual machines to be fetched as well. The following options; additonal_variables (all top level keys are now set as host_vars) and filters (these are set within the query now).

New Modules
-----------

- networktocode.nautobot.relationship_association - Creates or removes a relationship association from Nautobot

v3.4.1
======

Release Summary
---------------

This release adds a deprecation notice for the GraphQL Inventory Plugin. There will be changes to the structure requiring changes to the inventory file.

Minor Changes
-------------

- (#132) Adds deprecation notice on GraphQL Inventory Plugin
- (#133) Update documentation for query_graphql module and add try/except for HTTP call.
- (#135) Account for bug in networktocode.nautobot.inventory for API bug in Nautobot 1.3.1 due to OpenAPI paths changing.
- Sanity tests and updates requested by Ansible for collection inclusion.

v3.4.0
======

Release Summary
---------------

This release only changes the GraphQL inventory plugin. It fixes the ansible_host by removing the CIDR. The last change is the ability to specify nested relationships as well as fields that don't have a relationship to other Nautobot objects such as serial, asset_tag, etc.

Minor Changes
-------------

- (#122) Add ability to add nested GraphQL relationships and non-relationship fields such as serial, asset_tag, etc.

Bugfixes
--------

- (#124) Removes CIDR from the ansible_host variable.

v3.3.1
======

Bugfixes
--------

- (#116) Fix graphql action plugin to support check mode
- (#119) Documentation fixes
- (#120) Documentation permission fixes

v3.3.0
======

Minor Changes
-------------

- (#110) Allow users to define any path for defining GroupBy Group names
- (#115) Documentation fixes

v3.2.1
======

Release Summary
---------------

Unbreak plugins/inventory/inventory.yml

Bugfixes
--------

- Remove bad code in plugins/inventory/inventory.yml when locally built to publish that prevented it from grabbing all hosts

v3.2.0
======

Release Summary
---------------

A few updates to the inventory plugins to support new options or require existing parameters.

Minor Changes
-------------

- (#105) Documentation updates
- (#107) Add `tenant_group` to `group_by` to `inventory` plugin
- (#108) Add choices to `group_by` in `gql_inventory` plugin
- (#109) token is explicitly required within `gql_inventory` plugin. (This was always true, but never enforced.)

v3.1.1
======

Release Summary
---------------

Quick bugfix release for not attempting to resolve IDs for fields that a user has passed in an ID/UUID for

Bugfixes
--------

- (#98) No longer attempts to resolve field ID/UUIDs if user passes an ID/UUID for a resolvable field

v3.1.0
======

Release Summary
---------------

Adds inventory plugin leveraging Nautobot's GraphQL API

Minor Changes
-------------

- (#53) Adds inventory plugin using GraphQL API

New Modules
-----------

Networktocode
~~~~~~~~~~~~~

nautobot
^^^^^^^^

- networktocode.nautobot.networktocode.nautobot.gql_inventory - Inventory plugin leveraging Nautobot's GraphQL API

v3.0.0
======

Release Summary
---------------

Updates format for modules to support Ansible 4 / ansible-core 2.11 arg spec verification changes

Major Changes
-------------

- (#66) Remove data sub-dictionary from modules

Minor Changes
-------------

- (#57) Adds nautobot-server module
- (#75) Device Interface module supports custom_fields

v2.0.1
======

Release Summary
---------------

Bug fix updates for label support and SSL version consistency

Bugfixes
--------

- (#44) Add Interface Label Support
- (#45) SSL Verify Keyword Consistency Update

v2.0.0
======

Release Summary
---------------

Bug fixes and removal of NAUTOBOT_API and NAUTOBOT_API_TOKEN

Major Changes
-------------

- (#33) Deprecates NAUTOBOT_API and NAUTOBOT_API_TOKEN environment variables

Bugfixes
--------

- (#26) Add missing description to tenant_group
- (#29) Add missing field to vlan_group
- (#32) Fixed query on Virtual Chassis
- (#35) Add Site, Device Tracebacks due to changes in Nautobot

v1.1.0
======

New Modules
-----------

Networktocode
~~~~~~~~~~~~~

nautobot
^^^^^^^^

- networktocode.nautobot.networktocode.nautobot.lookup_graphql - Lookup plugin to query Nautobot GraphQL API endpoint
- networktocode.nautobot.networktocode.nautobot.query_graphql - Action plugin to query Nautobot GraphQL API endpoint

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
