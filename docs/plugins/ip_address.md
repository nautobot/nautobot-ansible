# networktocode.nautobot.ip_address

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.ip_address`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates or removes IP addresses from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| address | str | 3.0.0 | Required if state is `present` |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 3.0.0 | The description of the interface |
| dns_name | str | 3.0.0 | Hostname or FQDN |
| namespace | str | 5.0.0 | namespace that IP address is associated with. IPs are unique per namespaces. |
| nat_inside | raw | 3.0.0 | The inside IP address this IP is assigned to |
| parent | raw | 3.0.0 | With state `new`, it will force to get the next available IP in this prefix. Required if state is `present` or `new` when no address is given. Unused if an address is specified. |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| role | raw | 3.0.0 | The role of the IP address |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the IP address Required if I(state=present) and does not exist yet |
| tenant | raw | 3.0.0 | The tenant that the device will be assigned to |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| type | str | 5.0.0 | The type of the IP address |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
- name: "Test Nautobot IP address module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create IP address within Nautobot with only required information
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        status: active
        state: present
    - name: Force to create (even if it already exists) the IP
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        state: new
    - name: Create the same IP under another namespace
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        namespace: MyNewNamespace
        state: new
    - name: Get a new available IP inside 192.168.1.0/24
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 192.168.1.0/24
        state: new
    - name: Delete IP address within nautobot
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        state: absent
    - name: Create IP address with several specified options in namespace Private
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.20
        tenant: Test Tenant
        status: Reserved
        namespace: Private
        role: Loopback
        description: Test description
        tags:
          - Schnozzberry
        state: present
    - name: Create IP address and assign a nat_inside IP
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.30
        nat_inside:
          address: 192.168.1.20
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| ip_address | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
