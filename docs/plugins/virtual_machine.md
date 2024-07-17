# networktocode.nautobot.virtual_machine

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.virtual_machine`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates, updates or removes virtual_machines from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| cluster | raw | 3.0.0 | The name of the cluster attach to the virtual machine |
| comments | str | 3.0.0 | Comments of the virtual machine |
| disk | int | 3.0.0 | Disk of the virtual machine (GB) |
| local_config_context_data | dict | 3.0.0 | configuration context of the virtual machine |
| memory | int | 3.0.0 | Memory of the virtual machine (MB) |
| name | str | 3.0.0 | The name of the virtual machine |
| platform | raw | 3.0.0 | The platform of the virtual machine |
| primary_ip4 | raw | 3.0.0 | Primary IPv4 address assigned to the virtual machine |
| primary_ip6 | raw | 3.0.0 | Primary IPv6 address assigned to the virtual machine |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| role | raw | 3.0.0 | The role of the virtual machine |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the virtual machine Required if I(state=present) and does not exist yet |
| tenant | raw | 3.0.0 | The tenant that the virtual machine will be assigned to |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |
| vcpus | int | 3.0.0 | Number of vcpus of the virtual machine |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create virtual machine within Nautobot with only required information
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        cluster: test cluster
        status: active
        state: present

    - name: Delete virtual machine within nautobot
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        state: absent

    - name: Create virtual machine with tags
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Another Test Virtual Machine
        cluster: test cluster
        status: active
        tags:
          - Schnozzberry
        state: present

    - name: Update vcpus, memory and disk of an existing virtual machine
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        cluster: test cluster
        vcpus: 8
        memory: 8
        disk: 8
        state: present
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| machine | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
