[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Nautobot modules for Ansible using Ansible Collections

To keep the code simple, we only officially support the two latest releases of Nautobot and don't guarantee backwards compatibility beyond that.

## Requirements

- Nautobot 1.0.0+ or the two latest Nautobot releases
- Python 3.6+
- Python modules: **pynautobot 1.0.0+**
- Ansible 2.9+
- Nautobot write-enabled token when using modules or read-only token for `lookup/inventory`

We have a new docs site live that can be found [here](https://nautobot-ansible.readthedocs.io/en/latest/).

> This is a fork of the netbox.netbox Ansible Galaxy collection found at [https://github.com/netbox-community/ansible_modules](https://github.com/netbox-community/ansible_modules) in February, 2021

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `develop` branch with a release.

If backwards incompatible changes are needed, we plan to deprecate the old behavior as early as possible. We also plan to backport at least bugfixes for the old major version for some time after releasing a new major version. We will not block community members from backporting other bugfixes and features from the latest stable version to older release branches, under the condition that these backports are of reasonable quality.
