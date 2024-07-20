# networktocode.nautobot.power_outlet

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.power_outlet`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes power outlets from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 3.0.0 | Description of the power outlet |
| device | raw | 3.0.0 | The device the power outlet is attached to |
| feed_leg | str | 3.0.0 | The phase, in case of three-phase feed |
| name | str | 3.0.0 | The name of the power outlet |
| power_port | raw | 3.0.0 | The attached power port |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| type | str | 3.0.0 | The type of the power outlet |
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
    - name: Create power port within Nautobot with only required information
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device: Test Device
        state: present

    - name: Update power port with other fields
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device: Test Device
        type: iec-60320-c6
        power_port: Test Power Port
        feed_leg: A
        description: power port description
        state: present

    - name: Delete power port within nautobot
      networktocode.nautobot.power_outlet:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Outlet
        device: Test Device
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| msg | str | Message indicating failure or info about what has been achieved | always |
| power_outlet | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
