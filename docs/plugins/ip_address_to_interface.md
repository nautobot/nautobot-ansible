# networktocode.nautobot.ip_address_to_interface

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.ip_address_to_interface`.

+++ 5.0.0
    Added in 5.0.0.

## Synopsis

- Creates or removes IP address to interface association from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| interface | raw | 5.0.0 | Device interface to associate with an IP. |
| ip_address | raw | 5.0.0 | IP address to associate with an interface. |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding, or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |
| vm_interface | raw | 5.0.0 | VM interface to associate with an IP. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot IP address to interface module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: "Add IP address on GigabitEthernet4 - test100"
      networktocode.nautobot.ip_address_to_interface:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        ip_address: "{{ ip_address['key'] }}"
        interface:
          name: GigabitEthernet4
          device: test100
      vars:
        ip_address: "{{ lookup('networktocode.nautobot.lookup', 'ip-addresses', api_endpoint=nautobot_url, token=nautobot_token, api_filter='address=10.100.0.1/32') }}"

    - name: "Delete IP address on GigabitEthernet4 - test100"
      networktocode.nautobot.ip_address_to_interface:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        ip_address: "{{ ip_address['key'] }}"
        interface:
          name: GigabitEthernet4
          device: test100
        state: absent
      vars:
        ip_address: "{{ lookup('networktocode.nautobot.lookup', 'ip-addresses', api_endpoint=nautobot_url, token=nautobot_token, api_filter='address=10.100.0.1/32') }}"


```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| ip_address_to_interface | dict | Serialized object as created or already existent within Nautobot | on creation |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Mikhail Yohman (@FragmentedPacket)
- Anthony Ruhier (@Anthony25)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
