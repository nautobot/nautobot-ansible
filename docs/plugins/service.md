# networktocode.nautobot.service

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.service`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.

## Synopsis

- Creates or removes service from Nautobot.

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str | 3.0.0 | Service description. |
| device | raw | 3.0.0 | Specifies on which device the service is running. |
| ip_addresses | raw | 3.0.0 | Specifies which IPaddresses to associate with service. |
| name | str | 3.0.0 | Name of the region to be created. |
| ports | list | 3.0.0 | Specifies which ports used by service (Nautobot 2.10 and newer). |
| protocol | raw | 3.0.0 | Specifies which protocol used by service. |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |
| virtual_machine | raw | 3.0.0 | Specifies on which virtual machine the service is running. |

## Tags

!!! note "Note"
    * This should be ran with connection C(local) and hosts C(localhost).
    * The module supports C(check_mode).

## Examples

```yaml

- name: "Create nautobot service"
  connection: local
  hosts: all
  gather_facts: False

  tasks:
    - name: Create service
      networktocode.nautobot.service:
        url: url
        token: token
        device: Test666
        name: node-exporter
        ports:
          - 9100
        protocol: TCP
        ip_addresses:
          - address: 127.0.0.1
        tags:
          - prometheus
        state: present

- name: "Delete nautobot service"
  connection: local
  hosts: all
  gather_facts: False

  tasks:
    - name: Delete service
      networktocode.nautobot.service:
        url: url
        token: token
        device: Test666
        name: node-exporter
        ports:
          - 9100
        protocol: TCP
        state: absent

```


## Authors

- Kulakov Ilya (@TawR1024)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
