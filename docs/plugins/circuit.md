# networktocode.nautobot.circuit

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.circuit`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates, updates or removes circuits from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| cid | str | 3.0.0 | The circuit id of the circuit |
| circuit_type | raw | 3.0.0 | The circuit type of the circuit |
| comments | str | 3.0.0 | Comments related to circuit |
| commit_rate | int | 3.0.0 | Commit rate of the circuit (Kbps) |
| description | str | 3.0.0 | Description of the circuit |
| install_date | str | 3.0.0 | The date the circuit was installed. e.g. YYYY-MM-DD |
| provider | raw | 3.0.0 | The provider of the circuit |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the circuit Required if I(state=present) and does not exist yet |
| tenant | raw | 3.0.0 | The tenant assigned to the circuit |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |

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
    - name: Create circuit within Nautobot with only required information
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        cid: Test Circuit
        provider: Test Provider
        circuit_type: Test Circuit Type
        status: active
        state: present

    - name: Update circuit with other fields
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
        cid: Test-Circuit-1000
        provider: Test Provider
        circuit_type: Test Circuit Type
        status: Active
        tenant: Test Tenant
        install_date: "2018-12-25"
        commit_rate: 10000
        description: Test circuit
        comments: "FAST CIRCUIT"
        state: present

    - name: Delete circuit within nautobot
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        cid: Test-Circuit-1000
        state: absent
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| circuit | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
