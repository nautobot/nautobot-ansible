# networktocode.nautobot.cluster

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.cluster`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes clusters from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| cluster_group | raw | 3.0.0 | group of the cluster |
| cluster_type | raw | 3.0.0 | type of the cluster. Required if _state=present_ and the cluster does not exist yet |
| comments | str | 3.0.0 | Comments that may include additional information in regards to the cluster |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| location | raw | 3.0.0 | Cluster location. |
| name | str | 3.0.0 | The name of the cluster |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| tenant | raw | 3.0.0 | Tenant the cluster will be assigned to. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the `NAUTOBOT_TOKEN` environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the `NAUTOBOT_URL` environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the `NAUTOBOT_VALIDATE_CERTS` environment variable is configured. |

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
    - name: Create cluster within Nautobot with only required information
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster
        cluster_type: libvirt
        state: present

    - name: Delete cluster within nautobot
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster
        state: absent

    - name: Create cluster with tags
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Another Test Cluster
        cluster_type: libvirt
        tags:
          - Schnozzberry
        state: present

    - name: Update the group and location of an existing cluster
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster
        cluster_type: qemu
        cluster_group: GROUP
        location:
          name: My Location
          parent: Parent Location
        state: present

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| cluster | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Gaelle MANGIN (@gmangin)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
