# networktocode.nautobot.circuit_termination

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.circuit_termination`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes circuit terminations from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| circuit | raw | 3.0.0 | The circuit to assign to circuit termination |
| description | str | 3.0.0 | Description of the circuit termination |
| location | raw | 3.0.0 | The location the circuit termination will be assigned to |
| port_speed | int | 3.0.0 | The speed of the port (Kbps) |
| pp_info | str | 3.0.0 | Patch panel information |
| provider_network | raw | 4.2.0 | Connection to a provider_network type |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| term_side | str | 3.0.0 | The side of the circuit termination |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| upstream_speed | int | 3.0.0 | The upstream speed of the circuit termination |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |
| xconnect_id | str | 3.0.0 | The cross connect ID of the circuit termination |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create circuit termination within Nautobot with only required information
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: A
        location:
          name: My Location
          parent: Parent Location
        port_speed: 10000
        state: present

    - name: Create circuit termination to Provider Network
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: Z
        provider_network: 
          name: "Provider A"
        port_speed: 10000
        state: present

    - name: Update circuit termination with other fields
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: A
        upstream_speed: 1000
        xconnect_id: 10X100
        pp_info: PP10-24
        description: "Test description"
        state: present

    - name: Delete circuit termination within nautobot
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        circuit: Test Circuit
        term_side: A
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| circuit_termination | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Mikhail Yohman (@FragmentedPacket)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
