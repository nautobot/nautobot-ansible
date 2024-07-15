[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Nautobot Modules for Ansible using Ansible Collections

This collection provides Ansible modules to interact with Nautobot, an open-source Network Source of Truth and Network Automation Platform. The modules allow you to automate various tasks in Nautobot, such as managing devices, interfaces, IP addresses, and more.

To keep the code simple, we only officially support the two latest releases of Nautobot and don't guarantee backwards compatibility beyond that.

## Requirements

- Nautobot 1.0.0+ or the two latest Nautobot releases
- Python 3.6+
- Python modules: **pynautobot 1.0.0+** for Nautobot 1.x. For Nautobot 2.x please be using **pyantubot 2.x**
- Ansible 2.9+
- Nautobot write-enabled token when using modules or read-only token for `lookup/inventory` modules

We have a new docs site live that can be found [here](https://nautobot-ansible.readthedocs.io/en/latest/).

## Available Modules

Here is a list of available modules along with a brief description of each:

- **nautobot_device**: Manage devices in Nautobot.
- **nautobot_device_role**: Manage device roles in Nautobot.
- **nautobot_device_type**: Manage device types in Nautobot.
- **nautobot_interface**: Manage interfaces on devices in Nautobot.
- **nautobot_ip_address**: Manage IP addresses in Nautobot.
- **nautobot_site**: Manage sites in Nautobot.
- **nautobot_tenant**: Manage tenants in Nautobot.
- **nautobot_vlan**: Manage VLANs in Nautobot.
- **nautobot_virtual_machine**: Manage virtual machines in Nautobot.
- **nautobot_virtualization_cluster**: Manage virtualization clusters in Nautobot.
- **nautobot_cable**: Manage cables in Nautobot.
- **nautobot_circuit**: Manage circuits in Nautobot.
- **nautobot_power_feed**: Manage power feeds in Nautobot.
- **nautobot_rack**: Manage racks in Nautobot.
- **nautobot_rack_group**: Manage rack groups in Nautobot.
- **nautobot_inventory_item**: Manage inventory items in Nautobot.

## Releasing, Versioning, and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `develop` branch with a release.

If backwards incompatible changes are necessary, we plan to deprecate the old behavior as early as possible. We also plan to backport at least bugfixes for the old major version for some time after releasing a new major version. We will not block community members from backporting other bugfixes and features from the latest stable version to older release branches, under the condition that these backports are of reasonable quality. Some changes may not be able to be backported.

> Some changes that would require immediate patching that are breaking changes will fall to SemVer and constitute a breaking change. These will only be done when necessary, such as to support working with the most recent 3 versions of Ansible. Backporting these changes may not be possible.

> This is a fork of the netbox.netbox Ansible Galaxy collection found at [https://github.com/netbox-community/ansible_modules](https://github.com/netbox-community/ansible_modules) in February, 2021