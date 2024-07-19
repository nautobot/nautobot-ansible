# networktocode.nautobot.plugin

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.plugin`.

+++ 4.4.0 "Initial Modules Creation."
    Added in 4.4.0.

## Synopsis

- Creates, removes or updates various plugin objects in Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| attrs | dict | 4.4.0 | Object attributes other than identifier to create or update an object, like description, etc. |
| endpoint | str | 4.4.0 | Plugin object API endpoint |
| identifiers | dict | 4.4.0 | Plugin object identifier(s) like name, model, etc. |
| plugin | str | 4.4.0 | Plugin API base url |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags

!!! note "Note"
    * Task must have defined plugin base api url and object endpoint

## Examples

```yaml

- name: "Test Nautobot Plugin Module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create LCM CVE
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: nautobot-device-lifecycle-mgmt
        endpoint: cve
        identifiers:
          name: CVE-2020-7777
        attrs:
          published_date: 2020-09-25
          link: https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory
        state: present

    - name: Modify LCM CVE
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: nautobot-device-lifecycle-mgmt
        endpoint: cve
        identifiers:
          name: CVE-2020-7777
        attrs:
          published_date: 2020-09-25
          link: https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/12345678
        state: present

    - name: Delete LCM CVE
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: nautobot-device-lifecycle-mgmt
        endpoint: cve
        identifiers:
          name: CVE-2020-7777
        state: absent

    - name: Create GC compliance-feature
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: golden-config
        endpoint: compliance-feature
        ids:
          name: AAA
        attrs:
          description: "Authentication Administration Accounting"
        state: present
        
    - name: Create FW address-object
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: firewall
        endpoint: address-object
        ids:
          name: access-point
        attrs:
          ip_address:
            address: 10.0.0.0/32
        state: present

    - name: Delete FW address-object
      networktocode.nautobot.plugin:
        url: http://nautobot.local
        token: thisIsMyToken
        plugin: firewall
        endpoint: address-object
        ids:
          name: access-point
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| endpoint | dict | Serialized object as created/existent/updated/deleted within Nautobot | always |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Network to Code (@networktocode)
- Patryk Szulczewski (@pszulczewski)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
