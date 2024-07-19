# networktocode.nautobot.cable

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.cable`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes cables from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| color | str | 3.0.0 | The color of the cable |
| label | str | 3.0.0 | The label of the cable |
| length | int | 3.0.0 | The length of the cable |
| length_unit | str | 3.0.0 | The unit in which the length of the cable is measured |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| status | str | 3.0.0 | The status of the cable Required if I(state=present) and does not exist yet |
| termination_a | raw | 3.0.0 | The termination a |
| termination_a_type | str | 3.0.0 | The type of the termination a |
| termination_b | raw | 3.0.0 | The termination b |
| termination_b_type | str | 3.0.0 | The type of the termination b |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| type | str | 3.0.0 | The type of the cable |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

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
    - name: Create cable within Nautobot with only required information
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
        termination_a_type: dcim.interface
        termination_a:
          device: Test Nexus Child One
          name: Ethernet2/2
        termination_b_type: dcim.interface
        termination_b:
          device: Test Nexus Child One
          name: Ethernet2/1
        status: active
        state: present

    - name: Update cable with other fields
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
        termination_a_type: dcim.interface
        termination_a:
          device: Test Nexus Child One
          name: Ethernet2/2
        termination_b_type: dcim.interface
        termination_b:
          device: Test Nexus Child One
          name: Ethernet2/1
        type: mmf-om4
        status: planned
        label: label123
        color: abcdef
        length: 30
        length_unit: m
        state: present

    - name: Delete cable within nautobot
      networktocode.nautobot.cable:
        url: http://nautobot.local
        token: thisIsMyToken
        termination_a_type: dcim.interface
        termination_a:
          device: Test Nexus Child One
          name: Ethernet2/2
        termination_b_type: dcim.interface
        termination_b:
          device: Test Nexus Child One
          name: Ethernet2/1
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| cable | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
