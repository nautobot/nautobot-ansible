# networktocode.nautobot.device_interface_template

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.device_interface_template`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates or removes interfaces from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 5.2.0 | Description of the interface |
| device_type | raw | 3.0.0 | Name of the device the interface template will be associated with (case-sensitive) |
| label | str | 5.2.0 | Label of the interface template to be created |
| mgmt_only | bool | 3.0.0 | This interface template is used only for out-of-band management |
| name | str | 3.0.0 | Name of the interface template to be created |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| type | str | 3.0.0 | Form factor of the interface:
ex. 1000Base-T (1GE), Virtual, 10GBASE-T (10GE)
This has to be specified exactly as what is found within UI
 |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot interface template module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create interface template within Nautobot with only required information
      networktocode.nautobot.device_interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        device_type: Arista Test
        name: 10GBASE-T (10GE)
        type: 10gbase-t
        state: present
    - name: Delete interface template within nautobot
      networktocode.nautobot.device_interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        device_type: Arista Test
        name: 10GBASE-T (10GE)
        type: 10gbase-t
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| interface_template | dict | Serialized object as created or already existent within Nautobot | on creation |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
