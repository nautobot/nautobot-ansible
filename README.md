![https://github.com/nautobot/nautobot-ansible/actions](https://github.com/nautobot/nautobot-ansible/actions/workflows/trigger_scheduled.yml/badge.svg?branch=develop)
![https://docs.nautobot.com/projects/ansible/en/latest/](https://readthedocs.org/projects/nautobot-ansible/badge/)
![https://github.com/psf/black](https://img.shields.io/badge/code%20style-black-000000.svg)

# Nautobot Ansible

This collection provides Ansible plugins (modules, inventory, lookup/filters) to interact with Nautobot, an open-source Network Source of Truth and Network Automation Platform. The plugins allow you to automate various tasks in Nautobot, such as managing devices, interfaces, IP addresses, and more. By using these plugins, you can keep your Source of Truth (SOT) updated and ensure that your network data is accurate and consistent.

## Description

This collection provides Ansible plugins (modules, inventory, lookup/filters) to interact with Nautobot, an open-source Network Source of Truth and Network Automation Platform. The plugins allow you to automate various tasks in Nautobot, such as managing devices, interfaces, IP addresses, and more. By using these plugins, you can keep your Source of Truth (SOT) updated and ensure that your network data is accurate and consistent.

To keep the code simple, we only officially support the two latest releases of Nautobot and don't guarantee backwards compatibility beyond that.

Full documentation for this App can be found over on the [Nautobot Docs](https://docs.nautobot.com/projects/ansible/en/stable/) website:

- [Plugins Reference](https://docs.nautobot.com/projects/ansible/en/latest/networktocode.nautobot/) - Documentation (parameters, examples, return values) for all plugins included in the collection.
- [Installation Guide](https://docs.nautobot.com/projects/ansible/en/latest/getting_started/installation/)
- [Release Notes](https://docs.nautobot.com/projects/ansible/en/latest/release_notes/)

## Requirements

- Nautobot 1.0.0+ or the two latest Nautobot releases
- Python 3.11+ (aligned with ansible-core 2.18+ support)
- Python modules: **pynautobot 2.x+**
- Ansible 2.18+
- Nautobot write-enabled token when using `modules` or read-only token for `lookup/inventory`

## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```
ansible-galaxy collection install networktocode.nautobot
```

You can also include it in a requirements.yml file and install it with ansible-galaxy collection install -r requirements.yml, using the format:


```yaml
collections:
  - name: networktocode.nautobot
```

Note that if you install any collections from Ansible Galaxy, they will not be upgraded automatically when you upgrade the Ansible package.
To upgrade the collection to the latest available version, run the following command:

```
ansible-galaxy collection install networktocode.nautobot --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version 1.0.0:

```
ansible-galaxy collection install networktocode.nautobot:==1.0.0
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.


In addition to the above boilerplate, this section should include any additional details specific to your collection, and what to expect at each step and after installation. Be sure to include any information that supports the installation process, such as information about authentication and credentialing. 


## Use Cases

This collection provides Ansible plugins (modules, inventory, lookup/filters) to interact with Nautobot, an open-source Network Source of Truth and Network Automation Platform. The plugins allow you to automate various tasks in Nautobot, such as managing devices, interfaces, IP addresses, and more. By using these plugins, you can keep your Source of Truth (SOT) updated and ensure that your network data is accurate and consistent.

## Testing

Testing is completed via the GitHub actions located in the `.github/workflows` directory.

## Contributing

Check out the docs at https://docs.nautobot.com/projects/ansible/en/stable/getting_started/

## Support

For issues please use [GitHub Issues](https://github.com/nautobot/nautobot-ansible) to open any issue that you may have. Additional community is available at the [Network to Code Slack](https://networktocode.slack.com) and [sign up](https://slack.networktocode.com).

## Release Notes and Roadmap

Release notes are available at https://docs.nautobot.com/projects/ansible/en/stable/release_notes/

## Related Information

### Keeping Your Source of Truth Updated

Using the Nautobot Ansible modules, you can ensure that your Nautobot instance remains the authoritative Source of Truth (SOT) for your network. These modules allow for the automation of data input and updates, helping maintain consistency and accuracy across your network configuration and documentation. Whether you are provisioning new devices, updating interface configurations, or managing IP addresses, the Nautobot modules for Ansible provide the tools necessary to automate and streamline these tasks.

### Interacting with the Nautobot Platform

The modules in this collection enable seamless interaction with the Nautobot platform. With these modules, you can:

- Automate the provisioning and deprovisioning of network resources.
- Integrate Nautobot with your CI/CD pipelines to ensure up-to-date network configurations.
- Leverage Nautobot's API to gather real-time data for network monitoring and troubleshooting.
- Implement Infrastructure as Code (IaC) practices by managing Nautobot resources declaratively through Ansible playbooks.

### Available Modules

Here is a list of available modules along with a brief description of each:

- **networktocode.nautobot.device**: Manage devices in Nautobot.
- **networktocode.nautobot.device_role**: Manage device roles in Nautobot.
- **networktocode.nautobot.device_type**: Manage device types in Nautobot.
- **networktocode.nautobot.interface**: Manage interfaces on devices in Nautobot.
- **networktocode.nautobot.ip_address**: Manage IP addresses in Nautobot.
- **networktocode.nautobot.site**: Manage sites in Nautobot.
- **networktocode.nautobot.tenant**: Manage tenants in Nautobot.
- **networktocode.nautobot.vlan**: Manage VLANs in Nautobot.
- **networktocode.nautobot.virtual_machine**: Manage virtual machines in Nautobot.
- **networktocode.nautobot.virtualization_cluster**: Manage virtualization clusters in Nautobot.
- **networktocode.nautobot.cable**: Manage cables in Nautobot.
- **networktocode.nautobot.circuit**: Manage circuits in Nautobot.
- **networktocode.nautobot.power_feed**: Manage power feeds in Nautobot.
- **networktocode.nautobot.rack**: Manage racks in Nautobot.
- **networktocode.nautobot.rack_group**: Manage rack groups in Nautobot.
- **networktocode.nautobot.inventory_item**: Manage inventory items in Nautobot.

### Event-Driven Ansible (EDA)

This collection comes with a EDA source plugin that can monitor the Nautobot Change Log based on a configurable interval.

- **networktocode.nautobot.nautobot_changelog**: Listen for Change Log events and trigger actions against those.

More information on the Nautobot source plugin and EDA can be found [here](getting_started/how-to-use/eda.md).


### Releasing, Versioning, and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `develop` branch with a release.

If backwards incompatible changes are necessary, we plan to deprecate the old behavior as early as possible. We also plan to backport at least bugfixes for the old major version for some time after releasing a new major version. We will not block community members from backporting other bugfixes and features from the latest stable version to older release branches, under the condition that these backports are of reasonable quality. Some changes may not be able to be backported.

> Some changes that would require immediate patching that are breaking changes will fall to SemVer and constitute a breaking change. These will only be done when necessary, such as to support working with the most recent 3 versions of Ansible. Backporting these changes may not be possible.

### History

> This is a fork of the `netbox.netbox` Ansible Galaxy collection found at [https://github.com/netbox-community/ansible_modules](https://github.com/netbox-community/ansible_modules) in February, 2021.

## License Information

[GNU General Public License v3.0](https://github.com/nautobot/nautobot-ansible/blob/develop/LICENSE)
