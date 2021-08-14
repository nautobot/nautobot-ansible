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
