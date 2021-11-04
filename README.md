[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Nautobot modules for Ansible using Ansible Collections

To keep the code simple, we only officially support the two latest releases of Nautobot and don't guarantee backwards compatibility beyond that.

## Nautobot Roles

There are two roles that provide the model to handle a Nautobot installation onto an OS. The roles are used in conjunction with other roles provided by Geerlingguy, Redis and Postgres.

### Nautobot Install

The Nautobot Install role is used to install just the application. The currently supported installation method is to leverage Postgres, with a future feature request to support MySQL as well.

### Nautobot Web

This role installs NGINX to handle the web application front end. This is an optional add on that is currently _recommended_ but is not required.
## Requirements

- Nautobot 1.0.0+ or the two latest Nautobot releases
- Python 3.6+
- Python modules: **pynautobot 1.0.0+**
- Ansible 2.9+
- Nautobot write-enabled token when using modules or read-only token for `lookup/inventory`

We have a new docs site live that can be found [here](https://nautobot-ansible.readthedocs.io/en/latest/).

> This is a fork of the netbox.netbox Ansible Galaxy collection found at [https://github.com/netbox-community/ansible_modules](https://github.com/netbox-community/ansible_modules) in February, 2021