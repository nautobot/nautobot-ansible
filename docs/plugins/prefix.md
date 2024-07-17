# networktocode.nautobot.prefix

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.prefix`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates or removes prefixes from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 3.0.0 | The description of the prefix |
| first_available | bool | 3.0.0 | If `yes` and state `present`, if an parent is given, it will get the first available prefix of the given prefix_length inside the given parent (and namespace, if given). Unused with state `absent`. |
| ip_version | int | 5.0.0 | Specifies which address version the prefix prefix belongs to |
| location | raw | 3.0.0 | The single location the prefix will be associated to If you want to associate multiple locations, use the `prefix_location` module Using this parameter will override the `api_version` option to `2.0` |
| namespace | str | 5.0.0 | namespace that IP address is associated with. IPs are unique per namespaces. |
| parent | raw | 3.0.0 | Required if state is `present` and first_available is `yes`. Will get a new available prefix in this parent prefix. |
| prefix | raw | 3.0.0 | Required if state is `present` and first_available is False. Will allocate or free this prefix. |
| prefix_length | int | 3.0.0 | Required ONLY if state is `present` and first_available is `yes`. Will get a new available prefix of the given prefix_length in this parent prefix. |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| role | raw | 3.0.0 | The role of the prefix |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the prefix Required if I(state=present) and does not exist yet |
| tenant | raw | 3.0.0 | The tenant that the prefix will be assigned to |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| type | str | 5.0.0 | Prefix type |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |
| vlan | raw | 3.0.0 | The VLAN the prefix will be assigned to |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
- name: "Test Nautobot prefix module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create prefix within Nautobot with only required information
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 10.156.0.0/19
        status: active
        state: present

    - name: Delete prefix within nautobot
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 10.156.0.0/19
        state: absent

    - name: Create prefix with several specified options
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        family: 4
        prefix: 10.156.32.0/19
        location: My Location
        tenant: Test Tenant
        vlan:
          name: Test VLAN
          location: My Location
          tenant: Test Tenant
          vlan_group: Test Vlan Group
        status: Reserved
        role: Network of care
        description: Test description
        type: Pool
        tags:
          - Schnozzberry
        state: present

    - name: Get a new /24 inside 10.156.0.0/19 within Nautobot - Parent doesn't exist
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 10.156.0.0/19
        prefix_length: 24
        state: present
        first_available: yes

    - name: Create prefix within Nautobot with only required information
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: 10.156.0.0/19
        state: present

    - name: Get a new /24 inside 10.156.0.0/19 within Nautobot
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 10.156.0.0/19
        prefix_length: 24
        state: present
        first_available: yes

    - name: Get a new /24 inside 10.157.0.0/19 within Nautobot with additional values
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 10.157.0.0/19
        prefix_length: 24
        location:
          name: My Location
          parent: Parent Location
        state: present
        first_available: yes
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| prefix | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
