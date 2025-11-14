# networktocode.nautobot Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->

## [v6.0.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v6.0.0)

### Added

- [#639](https://github.com/nautobot/nautobot-ansible/issues/639) - Added the `device_cluster_assignment` module for managing device to cluster assignments in Nautobot.
- Added the `nautobot_status` lookup plugin to return the `/api/status/` information for the connected Nautobot instance.

### Changed

- [#637](https://github.com/nautobot/nautobot-ansible/issues/637) - Changed the value of `exclude_m2m` explicitly to `False` for all API endpoints in the inventory plugin.
- [#637](https://github.com/nautobot/nautobot-ansible/issues/637) - Changed the value of `exclude_m2m` explicitly to `False` for all modules.
- [#639](https://github.com/nautobot/nautobot-ansible/issues/639) - The `cluster`, `cluster_type`, and `cluster_group` fields for devices now return a list instead of a single value for the inventory plugin.

### Housekeeping

- [#598](https://github.com/nautobot/nautobot-ansible/issues/598) - Removed all version constraints from various test files.

### Removed

- [#639](https://github.com/nautobot/nautobot-ansible/issues/639) - Removed the `cluster` option from the `device` module. This was replaced with the `device_cluster_assignment` module.

## [v5.16.2](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.16.2)

### Fixed

- [#652](https://github.com/nautobot/nautobot-ansible/issues/652) - Fixed idempotency for the `device_interface` module when using `parent_interface` or `bridge` parameters.

## [v5.16.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.16.1)

### Documentation

- [#514](https://github.com/nautobot/nautobot-ansible/issues/514) - Fixed broken EDA link in docs.

### Fixed

- [#514](https://github.com/nautobot/nautobot-ansible/issues/514) - Fixed inability to set `validate_certs` for the `nautobot_changelog` EDA plugin.
- [#647](https://github.com/nautobot/nautobot-ansible/issues/647) - Fixed idempotency for the `custom_field_choice` module when using the custom field label instead of the UUID.

## [v5.16.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.16.0)

### Added

- [#595](https://github.com/nautobot/nautobot-ansible/issues/595) - Added the `device_family` module for creating, updating, and deleting device families in Nautobot.
- [#595](https://github.com/nautobot/nautobot-ansible/issues/595) - Added the `device_family` option to the `device_type` module for associating a device type with a device family.
- [#610](https://github.com/nautobot/nautobot-ansible/issues/610) - Added the `virtual_device_context` module for creating, updating, and deleting virtual device contexts in Nautobot.
- [#627](https://github.com/nautobot/nautobot-ansible/issues/627) - Added `custom_fields` option to multiple modules that support it yet were missing it.
- [#627](https://github.com/nautobot/nautobot-ansible/issues/627) - Added `tags` option to multiple modules that support it yet were missing it.

### Dependencies

- [#625](https://github.com/nautobot/nautobot-ansible/issues/625) - Updated `pynautobot` to `2.6.6` to fix an issue with parsing JSON fields (such as `constraints` on the Permission model).

### Fixed

- [#625](https://github.com/nautobot/nautobot-ansible/issues/625) - Fixed the argument type for the `constraints` parameter in the `admin_permission` module to `raw` instead of `json` for proper handling of dictionary and list constraints.

### Changed

- Updated CODEOWNERS to reflect current maintainers.

## [v5.15.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.15.0)

### Added

- [#140](https://github.com/nautobot/nautobot-ansible/issues/140) - Added the ability to use a saved GraphQL query from Nautobot when using the gql_inventory plugin.
- [#614](https://github.com/nautobot/nautobot-ansible/issues/614) - Added `id` to the default query for the gql_inventory plugin.

### Changed

- [#615](https://github.com/nautobot/nautobot-ansible/issues/615) - Changed the UUID used for devices with no name in the inventory plugin to the device ID instead of a random one.

### Documentation

- Added documentation for using Docker Compose overrides and a custom Nautobot init file.

### Fixed

- [#614](https://github.com/nautobot/nautobot-ansible/issues/614) - Fixed an issue where the gql_inventory plugin would fail if a device had no name.
- [#618](https://github.com/nautobot/nautobot-ansible/issues/618) - Fixed a bug when deleting certain objects with just an id.

### Housekeeping

- [#616](https://github.com/nautobot/nautobot-ansible/issues/616) - Changed the inventory tests to a single set of files that only run against the latest minor version of Nautobot.

## [v5.14.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.14.0)

### Added

- [#365](https://github.com/nautobot/nautobot-ansible/issues/365) - Added the `vrf_device_assignment` module for managing VRF to Device, VM or Virtual Device Context assignments in Nautobot.

## [v5.13.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.13.1)

### Added

- [#601](https://github.com/nautobot/nautobot-ansible/issues/601) - Added an option to the inventory plugins to disable the wrapping of unsafe variables.

### Dependencies

- Changed the minimum version of ansible-core to 2.17.

### Housekeeping

- [#602](https://github.com/nautobot/nautobot-ansible/issues/602) - Updated various documentation segments to pass ansible-lint.

## [v5.13.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.13.0)

### Release Summary

This release adds the ability to manage all objects by ID. You may now use the `id` parameter to update or delete existing objects. To accommodate for this, all previously required parameters are now optional. All required fields will be validated via the Nautobot API and returned as an error if they are not present.

### Added

- [#575](https://github.com/nautobot/nautobot-ansible/issues/575) - Added the `supported_data_rate` module for managing wireless supported data rates in Nautobot.
- [#576](https://github.com/nautobot/nautobot-ansible/issues/576) - Added the `radio_profile` module for managing radio profiles in Nautobot.
- [#577](https://github.com/nautobot/nautobot-ansible/issues/577) - Added the `wireless_network` module for managing wireless networks in Nautobot.
- [#589](https://github.com/nautobot/nautobot-ansible/issues/589), [#591](https://github.com/nautobot/nautobot-ansible/issues/591) - Added the `id` parameter to all object based modules.
- [#594](https://github.com/nautobot/nautobot-ansible/issues/594) - Added `software_version` and `software_image_files` parameters to the device module.

### Changed

- [#589](https://github.com/nautobot/nautobot-ansible/issues/589), [#591](https://github.com/nautobot/nautobot-ansible/issues/591) - Changed all required parameters to be optional for all object based modules. All required fields will be validated via the Nautobot API.

### Dependencies

- [#584](https://github.com/nautobot/nautobot-ansible/issues/584) - Updated to mkdocs-ansible-collection 1.1.0
- Updated pynautobot to v2.6.5 to incorporate fixes with choice list parsing and serializing.

### Fixed

- [#114](https://github.com/nautobot/nautobot-ansible/issues/114) - Fixed some variables (potentially unsafe) not being wrapped correctly in the `inventory` and `gql_inventory` plugins.
- Fixed an issue retrieving valid non-string (e.g. integer) choice values.

### Housekeeping

- [#542](https://github.com/nautobot/nautobot-ansible/issues/542) - Replaced black and bandit with ruff.
- [#586](https://github.com/nautobot/nautobot-ansible/issues/586) - Updated 2.4 inventory tests to account for new `module_family` field.
- Fixed sorting of duplicate interface and service names during the inventory integration tests.
- Fixed the `device` module integration tests to run certain tests on Nautobot 2.3+ to account for changes to the model validation.

## [v5.12.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.12.1)

### Fixed

- [#568](https://github.com/nautobot/nautobot-ansible/issues/568) - Fixed an issue with a utility function that was not able to sort some nested JSON custom fields.
- [#578](https://github.com/nautobot/nautobot-ansible/issues/578) - Fixed an issue with the inventory plugin when trying to group virtual machines by role or manufacturer.

## [v5.12.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.12.0)

### Added

- [#545](https://github.com/nautobot/nautobot-ansible/issues/545) - Added support for the `vrf` parameter to the `device_interface` and `vm_interface` modules.
- [#549](https://github.com/nautobot/nautobot-ansible/issues/549) - Added `label`, `parent`, `software_version`, and `software_image_files` options to the `inventory_item` module.
- [#550](https://github.com/nautobot/nautobot-ansible/issues/550) - Added option to fetch module interfaces in addition to device interfaces on the `networktocode.nautobot.inventory` plugin.
- [#559](https://github.com/nautobot/nautobot-ansible/issues/559) - Added the ability to rename variables set on the host for the inventory plugin.
- [#560](https://github.com/nautobot/nautobot-ansible/issues/560) - Added support for the `secrets_group` parameter to the `device` module.

### Dependencies

- [#555](https://github.com/nautobot/nautobot-ansible/issues/555) - Updated to mkdocs-ansible-collection 1.0.0

### Fixed

- [#526](https://github.com/nautobot/nautobot-ansible/issues/526) - Fixed the comparison of dictionaries with lists for better idempotency.
- [#548](https://github.com/nautobot/nautobot-ansible/issues/548) - Fixed identification of module interfaces when using `networktocode.nautobot.device_interfaces` plugin.
- [#550](https://github.com/nautobot/nautobot-ansible/issues/550) - Fixed parsing of inventory with `networktocode.nautobot.inventory` plugin when using `interfaces` option and module interfaces are present.

### Housekeeping

- [#547](https://github.com/nautobot/nautobot-ansible/issues/547) - Added Python 3.13 to the CI testing matrix.

## [v5.11.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.11.0)

### Added

- [#359](https://github.com/nautobot/nautobot-ansible/issues/359) - Added the `prefix_location` module for managing prefix to location assignments.
- [#531](https://github.com/nautobot/nautobot-ansible/issues/531) - Added the `secret` module for managing secrets in Nautobot.
- [#535](https://github.com/nautobot/nautobot-ansible/issues/535) - Added the `secrets_group` module for managing secrets groups in Nautobot.
- [#535](https://github.com/nautobot/nautobot-ansible/issues/535) - Added the `secrets_groups_association` module for associating secrets to secrets groups in Nautobot.

### Dependencies

- [#531](https://github.com/nautobot/nautobot-ansible/issues/531) - Updated pynautobot to v2.6.2 for proper idempotency of the `secret` module.

### Documentation

- [#525](https://github.com/nautobot/nautobot-ansible/issues/525) - Fixed a missing \` in the docs and added a little detail about the fact that the `.code-workspace` file is now an `.example`.
- Added documentation for running the tests manually via GitHub Actions.
- Updated the copyright documentation footer.

### Housekeeping

- [#527](https://github.com/nautobot/nautobot-ansible/issues/527) - Changed Python versions in test suite.
- [#527](https://github.com/nautobot/nautobot-ansible/issues/527) - Disabled duplicate keys in testing.
- [#528](https://github.com/nautobot/nautobot-ansible/issues/528) - Added a Manual CI workflow to test the collection with Galaxy Importer.
- [#537](https://github.com/nautobot/nautobot-ansible/issues/537) - Added the ability to skip specific test suites when running tests via `invoke unit` and `invoke integration`.

## [v5.10.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.10.0)

### Added

- [#517](https://github.com/nautobot/nautobot-ansible/issues/517) - Added Ansible Lint to the project.
- [#521](https://github.com/nautobot/nautobot-ansible/issues/521) - Added VLAN Group capability to vlan module.

### Changed

- [#515](https://github.com/nautobot/nautobot-ansible/issues/515) - Updated meta/runtime.yml minimum Ansible version to 2.16.

### Documentation

- [#518](https://github.com/nautobot/nautobot-ansible/issues/518) - Updated documentation on the primary README and the contributing.

### Housekeeping

- [#230](https://github.com/nautobot/nautobot-ansible/issues/230) - Added the towncrier library to dev dependencies to help generate release notes.
- [#230](https://github.com/nautobot/nautobot-ansible/issues/230) - Added documentation on how to create changelog fragments.
- [#512](https://github.com/nautobot/nautobot-ansible/issues/512) - Updated the directories included in the build process.
- Updated the release documentation to reflect the latest processes.
- Added links to existing entries in `CHANGELOG.md`.
- Fixed many ansible-lint and ansible-test issues.

## [v5.9.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.9.0)

### Release Summary

This is the first official release of an Ansible EDA Event Source plugin for Nautobot Changelog.

### New Event Source Plugins

- **networktocode.nautobot.nautobot_changelog**: Listen for Change Log events and trigger actions against those.

## [v5.8.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.8.1)

### Added

- [#502](https://github.com/nautobot/nautobot-ansible/issues/502) - Added the ability to look up IP Addresses by address and namespace for `ip_address_to_interface` module
- [#503](https://github.com/nautobot/nautobot-ansible/issues/503) - Added VS Code development workspace config file and documentation for use

## [v5.8.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.8.0)

### Minor Changes

- [#494](https://github.com/nautobot/nautobot-ansible/issues/494) - Updated `mkdocs-ansible-collection` dev dependency to `0.2.1` to fix documentation rendering issues
- [#497](https://github.com/nautobot/nautobot-ansible/issues/497) - Added integration tests for the `gql_inventory` plugin
- [#498](https://github.com/nautobot/nautobot-ansible/issues/498) - Added `network_driver` option to `platform` module
- [#499](https://github.com/nautobot/nautobot-ansible/issues/499) - Added `page_size` option to `gql_inventory` plugin to allow for pagination of large results

## [v5.7.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.7.0)

### New Modules

- networktocode.nautobot.controller_managed_device_groups - Creates or removes controller managed device groups within Nautobot
- networktocode.nautobot.software_version - Creates or removes software versions from Nautobot

### Minor Changes

- [#488](https://github.com/nautobot/nautobot-ansible/issues/488) - Fixed `module_bay_template` idempotency when duplicate bay names exist for multiple device or module types

## [v5.6.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.6.0)

### Minor Changes

- [#470](https://github.com/nautobot/nautobot-ansible/issues/470) - Dropped support for Python 3.10 to follow ansible-core 2.18
- [#472](https://github.com/nautobot/nautobot-ansible/issues/472) - Added documentation on using custom fields in compose variables with the `inventory` plugin
- [#474](https://github.com/nautobot/nautobot-ansible/issues/474) - Fixed `lookup` plugin to properly handle templated variables in `api_filter`
- [#475](https://github.com/nautobot/nautobot-ansible/issues/475) - Added documentation for the `device_interface` module that `type` is required when creating a new interface
- [#477](https://github.com/nautobot/nautobot-ansible/issues/477) - Fixed query example in the `lookup_graphql` plugin documentation for compatibility with Nautobot 2.X
- [#478](https://github.com/nautobot/nautobot-ansible/issues/478) - Fixed the `cable` module to properly work with all cable types
- [#480](https://github.com/nautobot/nautobot-ansible/issues/480) - Fixed environment variable fallback for `url` and `token` in all modules
- [#481](https://github.com/nautobot/nautobot-ansible/issues/481) - Fixed environment variable fallback for `validate_certs` in all modules

## [v5.5.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.5.0)

### New Modules

- networktocode.nautobot.job_button - Creates or removes job buttons from Nautobot
- networktocode.nautobot.dynamic_group - Creates or removes dynamic groups from Nautobot
- networktocode.nautobot.static_group_association - Creates or removes static group associations from Nautobot
- networktocode.nautobot.metadata_type - Creates or removes metadata types from Nautobot
- networktocode.nautobot.metadata_choice - Creates or removes metadata choices from Nautobot
- networktocode.nautobot.object_metadata - Creates or removes object metadata from Nautobot

### Minor Changes

- [#464](https://github.com/nautobot/nautobot-ansible/issues/464) - Added full support for caching to GraphQL Inventory plugin
- [#465](https://github.com/nautobot/nautobot-ansible/issues/465) - Changed `parent_location_type` to allow for explicit name attribute lookup

## [v5.4.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.4.0)

### New Modules

- networktocode.nautobot.cloud_account - Creates or removes cloud accounts from Nautobot
- networktocode.nautobot.cloud_network - Creates or removes cloud networks from Nautobot
- networktocode.nautobot.cloud_resource_type - Creates or removes cloud resource types from Nautobot
- networktocode.nautobot.cloud_service - Creates or removes cloud services from Nautobot
- networktocode.nautobot.cloud_service_network_assignment - Creates or removes cloud service network assignments from Nautobot
- networktocode.nautobot.cloud_network_prefix_assignment - Creates or removes cloud network prefix assignments from Nautobot
- networktocode.nautobot.module - Creates or removes modules from Nautobot
- networktocode.nautobot.module_type - Creates or removes module types from Nautobot
- networktocode.nautobot.module_bay - Creates or removes module bays from Nautobot
- networktocode.nautobot.module_bay_template - Creates or removes module bay templates from Nautobot

### Minor Changes

- [#431](https://github.com/nautobot/nautobot-ansible/issues/431) - Added tags and custom fields options to `cable` module
- [#433](https://github.com/nautobot/nautobot-ansible/issues/433) - Added role option to `device_interface` module
- [#438](https://github.com/nautobot/nautobot-ansible/issues/438) - Added cloud_network option to `circuit_termination` module
- [#446](https://github.com/nautobot/nautobot-ansible/issues/446) - Added module option to multiple existing modules
- [#449](https://github.com/nautobot/nautobot-ansible/issues/449) - Changed lookup plugin to allow for multiple `id` filters

## [v5.3.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.3.1)

### Minor Changes

- [#422](https://github.com/nautobot/nautobot-ansible/issues/422) - Fixed `admin_permission` module to properly convert list of groups to UUIDs
- [#427](https://github.com/nautobot/nautobot-ansible/issues/427) - Fixed setting of `default_ip_version` option. Fixed logic in `add_ip_address` that sets Ansible `host` values

## [v5.3.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.3.0)

### New Modules

- networktocode.nautobot.vlan_location - Creates or removes Location assignments to VLANs from Nautobot
- networktocode.nautobot.contact - Creates or removes contacts from Nautobot
- networktocode.nautobot.team - Creates or removes teams from Nautobot
- networktocode.nautobot.controller - Creates or removes controllers from Nautobot
- networktocode.nautobot.admin_user - Creates or removes users from Nautobot
- networktocode.nautobot.admin_group - Creates or removes groups from Nautobot
- networktocode.nautobot.admin_permission - Creates or removes permissions from Nautobot

### Minor Changes

- [#352](https://github.com/nautobot/nautobot-ansible/issues/352) - Added IPv6 support as the default IP version for `gql_inventory` plugin
- [#415](https://github.com/nautobot/nautobot-ansible/issues/415) - Added `role` option to `vm_interface` module
- [#416](https://github.com/nautobot/nautobot-ansible/issues/416) - Fixed `location_type` idempotency for `location` module

## [v5.2.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.2.1)

### Minor Changes

- [#345](https://github.com/nautobot/nautobot-ansible/issues/345) - Added `NAUTOBOT_VALIDATE_CERTS` environment variable to disable SSL verification
- [#348](https://github.com/nautobot/nautobot-ansible/issues/348) - Fixed GraphQL Inventory plugin bug when device platform is None

## [v5.2.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.2.0)

### Minor Changes

- [#310](https://github.com/nautobot/nautobot-ansible/issues/310) - Fixed `parent` for location_type to convert to UUID for idempotency
- [#319](https://github.com/nautobot/nautobot-ansible/issues/319) - Added `custom_fields` to `tag`, `vlan_group` and `role` modules
- [#321](https://github.com/nautobot/nautobot-ansible/issues/321) - Updated documentation and examples for the `lookup` plugin
- [#323](https://github.com/nautobot/nautobot-ansible/issues/323) - Added constructed features and inventory cache to the `gql_inventory` plugin
- [#335](https://github.com/nautobot/nautobot-ansible/issues/335) - Fixed custom field idempotency for various modules
- [#336](https://github.com/nautobot/nautobot-ansible/issues/336) - Added `custom_fields` to the `inventory_item` module
- [#338](https://github.com/nautobot/nautobot-ansible/issues/338) - Added `num_retries` to the `lookup` plugin
- [#340](https://github.com/nautobot/nautobot-ansible/issues/340) - Added `label` and `description` to the `device_interface_template` module

## [v5.1.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.1.1)

### Minor Changes

- [#298](https://github.com/nautobot/nautobot-ansible/issues/298) - Removes `status` option from being required unless creating a new object for various modules
- [#299](https://github.com/nautobot/nautobot-ansible/issues/299) - Added example for using the `depth` option in the `lookup` module
- [#304](https://github.com/nautobot/nautobot-ansible/issues/304) - Fixed the ability to look up `parent_location` by name instead of UUID in the `location` module

## [v5.1.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.1.0)

### Release Summary

This release adds various new modules and includes some bug fixes and minor changes.

### New Modules

- networktocode.nautobot.device_redundancy_group - Creates or removes device redundancy groups from Nautobot
- networktocode.nautobot.custom_field - Creates or removes custom fields from Nautobot
- networktocode.nautobot.custom_field_choice - Creates or removes custom field choices from Nautobot
- networktocode.nautobot.namespace - Creates or removes namespaces from Nautobot

### Minor Changes

- [#273](https://github.com/nautobot/nautobot-ansible/issues/273) - Added custom_fields option to the vm_interface module.
- [#275](https://github.com/nautobot/nautobot-ansible/issues/275) - Added additional options to the location module that were originally on site and region in Nautobot 1.X.
- [#283](https://github.com/nautobot/nautobot-ansible/issues/283) - Fixed the following lookup plugins to properly use a dash instead of an underscore:
    - `location-types`
    - `provider-networks`
    - `relationship-associations`
- [#287](https://github.com/nautobot/nautobot-ansible/issues/287) - Adds the ability to use the UUID, name or name and parent (as key/value pairs) for the `location` parameter in various modules.

## [v5.0.2](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.0.2)

### Minor Changes

- [#248](https://github.com/nautobot/nautobot-ansible/issues/248) - Remove choices from various modules, in favor of pynaubot choices() method.
- [#269](https://github.com/nautobot/nautobot-ansible/issues/269) - Fix SSL verification.

## [v5.0.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.0.1)

### Minor Changes

- [#257](https://github.com/nautobot/nautobot-ansible/issues/257) - Fix plugin module.

## [v5.0.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v5.0.0)

### Release Summary

This release updates collection code for compatibility code with Nautobot 2.0, where API has breaking changes.

### Breaking Changes / Porting Guide

- [#234](https://github.com/nautobot/nautobot-ansible/issues/234) - Updates for Nautobot 2.0 Compatibility

### New Modules

- networktocode.nautobot.ip_address_to_interface - Creates or removes associations between IP and interface.
- networktocode.nautobot.role - Creates or removes a role. Collapsed from several role modules in DCIM and IPAM.

## [v4.5.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.5.0)

### Release Summary

Fixes error handling in inventory to not erase inventories, minor bug fixes, and introduces Plugin module

### Minor Changes

- [#211](https://github.com/nautobot/nautobot-ansible/issues/211) - Removes codecov from dev dependencies
- [#217](https://github.com/nautobot/nautobot-ansible/issues/217) - Fixes and enables testing for Nautobot 1.5
- [#220](https://github.com/nautobot/nautobot-ansible/issues/220) - Adds status option to device_interface module

### Bugfixes

- [#209](https://github.com/nautobot/nautobot-ansible/issues/209) - Catches HTTPError for `query_graphql` and fails to enable ansible retries
- [#223](https://github.com/nautobot/nautobot-ansible/issues/223) - Inventory Hosts Empty On Error
- [#228](https://github.com/nautobot/nautobot-ansible/issues/228) - Fixes graphql inventory grouping by tags

## [v4.4.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.4.0)

### Minor Changes

- [#203](https://github.com/nautobot/nautobot-ansible/issues/203) - Adds plugin module
- [#209](https://github.com/nautobot/nautobot-ansible/issues/209) - Catches HTTPError for GraphQL query and enables Ansible retries
- [#211](https://github.com/nautobot/nautobot-ansible/issues/211) - Removes codecov from dev dependencies

## [v4.3.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.3.1)

### Bugfixes

- [#196](https://github.com/nautobot/nautobot-ansible/issues/196) - Virtual Chassis return multiple result at times

## [v4.3.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.3.0)

### Minor Changes

- [#185](https://github.com/nautobot/nautobot-ansible/issues/185) - Updated Doc Fragments
- [#187](https://github.com/nautobot/nautobot-ansible/issues/187) - Updated Tag documentation
- [#191](https://github.com/nautobot/nautobot-ansible/issues/191) - Added locations and location_type modules

## [v4.2.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.2.0)

### Minor Changes

- [#171](https://github.com/nautobot/nautobot-ansible/issues/171) - Add provider_network to circuit_termination module
- [#172](https://github.com/nautobot/nautobot-ansible/issues/172) - Add description to manufacturer

## [v4.1.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.1.1)

### Release Summary

Fix incorrect filter parameters

### Bugfixes

- [#163](https://github.com/nautobot/nautobot-ansible/issues/163) - Fix bad filter params due to `STRICT_FILTERING` being enabled in Nautobot 1.4.

## [v4.1.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.1.0)

### Release Summary

Fix minor bugs and add API versioning to collection.

### Minor Changes

- [#139](https://github.com/nautobot/nautobot-ansible/issues/139) - - Add API versioning to compatible plugins.

### Bugfixes

- [#159](https://github.com/nautobot/nautobot-ansible/issues/159) - Lookup - Fix `api_filter` to not attempt to convert UUIDs to integers from legacy forked code.

## [v4.0.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.0.1)

### Release Summary

Fixes GraphQL inventory plugin bugs and RTD builds.

### Bugfixes

- [#150](https://github.com/nautobot/nautobot-ansible/issues/150) - GraphQL inventory plugin - boolean filters are invalid
- [#151](https://github.com/nautobot/nautobot-ansible/issues/151) - GraphQL inventory plugin - using group_by can crash if there are empty values
- [#154](https://github.com/nautobot/nautobot-ansible/issues/154) - Fixes antsibull import for RTD builds

## [v4.0.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v4.0.0)

### Release Summary

This release refactors the GraphQL inventory plugin to allow fetching virtual machines and a more flexible approach to allow users to use most of GraphQL's native capabilities.

### Breaking Changes / Porting Guide

- [#130](https://github.com/nautobot/nautobot-ansible/issues/130) - Refactors GraphQL Inventory plugin to allow custom GraphQL queries with nested levels. Allows virtual machines to be fetched as well. The following options; additional_variables (all top level keys are now set as host_vars) and filters (these are set within the query now).

### New Modules

- networktocode.nautobot.relationship_association - Creates or removes a relationship association from Nautobot

## [v3.4.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.4.1)

### Release Summary

This release adds a deprecation notice for the GraphQL Inventory Plugin. There will be changes to the structure requiring changes to the inventory file.

### Minor Changes

- [#132](https://github.com/nautobot/nautobot-ansible/issues/132) - Adds deprecation notice on GraphQL Inventory Plugin
- [#133](https://github.com/nautobot/nautobot-ansible/issues/133) - Update documentation for query_graphql module and add try/except for HTTP call.
- [#135](https://github.com/nautobot/nautobot-ansible/issues/135) - Account for bug in networktocode.nautobot.inventory for API bug in Nautobot 1.3.1 due to OpenAPI paths changing.
- Sanity tests and updates requested by Ansible for collection inclusion.

## [v3.4.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.4.0)

### Release Summary

This release only changes the GraphQL inventory plugin. It fixes the ansible_host by removing the CIDR. The last change is the ability to specify nested relationships as well as fields that don't have a relationship to other Nautobot objects such as serial, asset_tag, etc.

### Minor Changes

- [#122](https://github.com/nautobot/nautobot-ansible/issues/122) - Add ability to add nested GraphQL relationships and non-relationship fields such as serial, asset_tag, etc.

### Bugfixes

- [#124](https://github.com/nautobot/nautobot-ansible/issues/124) - Removes CIDR from the ansible_host variable.

## [v3.3.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.3.1)

### Bugfixes

- [#116](https://github.com/nautobot/nautobot-ansible/issues/116) - Fix graphql action plugin to support check mode
- [#119](https://github.com/nautobot/nautobot-ansible/issues/119) - Documentation fixes
- [#120](https://github.com/nautobot/nautobot-ansible/issues/120) - Documentation permission fixes

## [v3.3.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.3.0)

### Minor Changes

- [#110](https://github.com/nautobot/nautobot-ansible/issues/110) - Allow users to define any path for defining GroupBy Group names
- [#115](https://github.com/nautobot/nautobot-ansible/issues/115) - Documentation fixes

## [v3.2.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.2.1)

### Release Summary

Unbreak plugins/inventory/inventory.yml

### Bugfixes

- Remove bad code in plugins/inventory/inventory.yml when locally built to publish that prevented it from grabbing all hosts

## [v3.2.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.2.0)

### Release Summary

A few updates to the inventory plugins to support new options or require existing parameters.

### Minor Changes

- [#105](https://github.com/nautobot/nautobot-ansible/issues/105) - Documentation updates
- [#107](https://github.com/nautobot/nautobot-ansible/issues/107) - Add `tenant_group` to `group_by` to `inventory` plugin
- [#108](https://github.com/nautobot/nautobot-ansible/issues/108) - Add choices to `group_by` in `gql_inventory` plugin
- [#109](https://github.com/nautobot/nautobot-ansible/issues/109) - token is explicitly required within `gql_inventory` plugin. (This was always true, but never enforced.)

## [v3.1.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.1.1)

### Release Summary

Quick bugfix release for not attempting to resolve IDs for fields that a user has passed in an ID/UUID for

### Bugfixes

- [#98](https://github.com/nautobot/nautobot-ansible/issues/98) - No longer attempts to resolve field ID/UUIDs if user passes an ID/UUID for a resolvable field

## [v3.1.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.1.0)

### Release Summary

Adds inventory plugin leveraging Nautobot's GraphQL API

### Minor Changes

- [#53](https://github.com/nautobot/nautobot-ansible/issues/53) - Adds inventory plugin using GraphQL API

### New Modules

- networktocode.nautobot.gql_inventory - Inventory plugin leveraging Nautobot's GraphQL API

## [v3.0.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v3.0.0)

### Release Summary

Updates format for modules to support Ansible 4 / ansible-core 2.11 arg spec verification changes

### Major Changes

- [#66](https://github.com/nautobot/nautobot-ansible/issues/66) - Remove data sub-dictionary from modules

### Minor Changes

- [#57](https://github.com/nautobot/nautobot-ansible/issues/57) - Adds nautobot-server module
- [#75](https://github.com/nautobot/nautobot-ansible/issues/75) - Device Interface module supports custom_fields

## [v2.0.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v2.0.1)

### Release Summary

Bug fix updates for label support and SSL version consistency

### Bugfixes

- [#44](https://github.com/nautobot/nautobot-ansible/issues/44) - Add Interface Label Support
- [#45](https://github.com/nautobot/nautobot-ansible/issues/45) - SSL Verify Keyword Consistency Update

## [v2.0.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v2.0.0)

### Release Summary

Bug fixes and removal of NAUTOBOT_API and NAUTOBOT_API_TOKEN

### Major Changes

- [#33](https://github.com/nautobot/nautobot-ansible/issues/33) - Deprecates NAUTOBOT_API and NAUTOBOT_API_TOKEN environment variables

### Bugfixes

- [#26](https://github.com/nautobot/nautobot-ansible/issues/26) - Add missing description to tenant_group
- [#29](https://github.com/nautobot/nautobot-ansible/issues/29) - Add missing field to vlan_group
- [#32](https://github.com/nautobot/nautobot-ansible/issues/32) - Fixed query on Virtual Chassis
- [#35](https://github.com/nautobot/nautobot-ansible/issues/35) - Add Site, Device Tracebacks due to changes in Nautobot

## [v1.1.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v1.1.0)

### New Lookup Plugins

- networktocode.nautobot.lookup_graphql - Lookup plugin to query Nautobot GraphQL API endpoint

### New Action Plugins

- networktocode.nautobot.query_graphql - Action plugin to query Nautobot GraphQL API endpoint

## [v1.0.4](https://github.com/nautobot/nautobot-ansible/releases/tag/v1.0.4)

### Bugfixes

- [#22](https://github.com/nautobot/nautobot-ansible/pull/22) - Added check for UUIDs when checking for isinstance(int)
- [#23](https://github.com/nautobot/nautobot-ansible/pull/23) - ip_address - Removed interface option

## [v1.0.3](https://github.com/nautobot/nautobot-ansible/releases/tag/v1.0.3)

### Bugfixes

- [#17](https://github.com/nautobot/nautobot-ansible/pull/17) - Validate if value is already a UUID, return UUID and do not attempt to resolve

## [v1.0.2](https://github.com/nautobot/nautobot-ansible/releases/tag/v1.0.2)

### Bugfixes

- Remove code related to fetching secrets due to secrets not existing in Nautobot.

## [v1.0.1](https://github.com/nautobot/nautobot-ansible/releases/tag/v1.0.1)

### Release Summary

Removes dependency on ansible.netcommon and uses builtin ipaddress module

## [v1.0.0](https://github.com/nautobot/nautobot-ansible/releases/tag/v1.0.0)

### Release Summary

This is the first official release of an Ansible Collection for Nautobot.
This project is forked from the ``netbox.netbox`` Ansible Collection.

### New Lookup Plugins

- networktocode.nautobot.lookup - Queries and returns elements from Nautobot

### New Modules

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
