[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Nautobot Modules for Ansible using Ansible Collections

This collection provides Ansible modules to interact with Nautobot, an open-source Network Source of Truth and Network Automation Platform. The modules allow you to automate various tasks in Nautobot, such as managing devices, interfaces, IP addresses, and more. By using these modules, you can keep your Source of Truth (SOT) updated and ensure that your network data is accurate and consistent.

To keep the code simple, we only officially support the two latest releases of Nautobot and don't guarantee backwards compatibility beyond that.

## Requirements

- Nautobot 1.0.0+ or the two latest Nautobot releases
- Python 3.6+
- Python modules: **pynautobot 2.x+**
- Ansible 2.9+
- Nautobot write-enabled token when using modules or read-only token for `lookup/inventory`

We have a new docs site live that can be found [here](https://nautobot-ansible.readthedocs.io/en/latest/).

## Keeping Your Source of Truth Updated

Using the Nautobot Ansible modules, you can ensure that your Nautobot instance remains the authoritative Source of Truth (SOT) for your network. These modules allow for the automation of data input and updates, helping maintain consistency and accuracy across your network configuration and documentation. Whether you are provisioning new devices, updating interface configurations, or managing IP addresses, the Nautobot modules for Ansible provide the tools necessary to automate and streamline these tasks.

## Interacting with the Nautobot Platform

The modules in this collection enable seamless interaction with the Nautobot platform. With these modules, you can:

- Automate the provisioning and deprovisioning of network resources.
- Integrate Nautobot with your CI/CD pipelines to ensure up-to-date network configurations.
- Leverage Nautobot's API to gather real-time data for network monitoring and troubleshooting.
- Implement Infrastructure as Code (IaC) practices by managing Nautobot resources declaratively through Ansible playbooks.

## Available Modules

Here is a list of available modules along with a brief description of each:

- **nautobot.device**: Manage devices in Nautobot.
- **nautobot.device_role**: Manage device roles in Nautobot.
- **nautobot.device_type**: Manage device types in Nautobot.
- **nautobot.interface**: Manage interfaces on devices in Nautobot.
- **nautobot.ip_address**: Manage IP addresses in Nautobot.
- **nautobot.site**: Manage sites in Nautobot.
- **nautobot.tenant**: Manage tenants in Nautobot.
- **nautobot.vlan**: Manage VLANs in Nautobot.
- **nautobot.virtual_machine**: Manage virtual machines in Nautobot.
- **nautobot.virtualization_cluster**: Manage virtualization clusters in Nautobot.
- **nautobot.cable**: Manage cables in Nautobot.
- **nautobot.circuit**: Manage circuits in Nautobot.
- **nautobot.power_feed**: Manage power feeds in Nautobot.
- **nautobot.rack**: Manage racks in Nautobot.
- **nautobot.rack_group**: Manage rack groups in Nautobot.
- **nautobot.inventory_item**: Manage inventory items in Nautobot.

## Releasing, Versioning, and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `develop` branch with a release.

If backwards incompatible changes are necessary, we plan to deprecate the old behavior as early as possible. We also plan to backport at least bugfixes for the old major version for some time after releasing a new major version. We will not block community members from backporting other bugfixes and features from the latest stable version to older release branches, under the condition that these backports are of reasonable quality. Some changes may not be able to be backported.

> Some changes that would require immediate patching that are breaking changes will fall to SemVer and constitute a breaking change. These will only be done when necessary, such as to support working with the most recent 3 versions of Ansible. Backporting these changes may not be possible.

## History

> This is a fork of the netbox.netbox Ansible Galaxy collection found at [https://github.com/netbox-community/ansible_modules](https://github.com/netbox-community/ansible_modules) in February, 2021