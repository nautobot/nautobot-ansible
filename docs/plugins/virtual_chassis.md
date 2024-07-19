# networktocode.nautobot.virtual_chassis

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.virtual_chassis`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes virtual chassis from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| domain | str | 3.0.0 | domain of the virtual chassis |
| master | raw | 3.0.0 | The master device the virtual chassis is attached to |
| name | str | 3.0.0 | Name |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
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
    - name: Create virtual chassis within Nautobot with only required information
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "Virtual Chassis 1"
        state: present

    - name: Update virtual chassis with other fields
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "Virtual Chassis 1"
        master: Test Device
        domain: Domain Text
        state: present

    - name: Delete virtual chassis within nautobot
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "Virtual Chassis 1"
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| msg | str | Message indicating failure or info about what has been achieved | always |
| virtual_chassis | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
