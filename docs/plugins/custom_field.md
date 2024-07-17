# networktocode.nautobot.custom_field

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.custom_field`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates or removes custom fields from Nautobot

## Requirements

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| advanced_ui | bool | 5.1.0 | Whether or not to display this field in the advanced tab |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| content_types | list | 5.1.0 | Content types that this field should be available for Required if I(state=present) and the custom field does not exist yet |
| default | raw | 5.1.0 | Default value for this field when editing models Must be in JSON format |
| description | str | 5.1.0 | Description of this field Also used as the help text when editing models using this custom field Markdown is supported |
| filter_logic | str | 5.1.0 | Filter logic to apply when filtering models based on this field Only compatible with I(type=text), I(type=url) and I(type=json) |
| grouping | str | 5.1.0 | Human-readable grouping that this custom field belongs to |
| key | str | 5.1.0 | Internal name of this field Required if I(state=present) and the custom field does not exist yet |
| label | str | 5.1.0 | Name of the field as displayed to users |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| required | bool | 5.1.0 | Whether or not a value is required for this field when editing models |
| state | str |  | Use `present` or `absent` for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| type | str | 5.1.0 | Data type of this field Required if I(state=present) and the custom field does not exist yet I(type=select) and I(type=multi-select) require choices to be defined separately with the I(custom_field_choice) module |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |
| validation_maximum | int | 5.1.0 | Maximum value allowed for this field Only compatible with I(type=integer) |
| validation_minimum | int | 5.1.0 | Minimum value allowed for this field Only compatible with I(type=integer) |
| validation_regex | str | 5.1.0 | Regular expression that this field must match Only compatible with I(type=text) |
| weight | int | 5.1.0 | Position this field should be displayed in |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
- name: Create custom field within Nautobot with only required information
  networktocode.nautobot.custom_field:
    url: http://nautobot.local
    token: thisIsMyToken
    label: My Custom Field
    key: my_custom_field
    type: text
    state: present

- name: Create custom field within Nautobot with all information
  networktocode.nautobot.custom_field:
    url: http://nautobot.local
    token: thisIsMyToken
    label: My Custom Field
    grouping: My Grouping
    key: my_custom_field
    type: text
    weight: 100
    description: My Description
    required: true
    default: My Default
    filter_logic: loose
    advanced_ui: true
    content_types:
      - dcim.device
    validation_minimum: 0
    validation_maximum: 100
    validation_regex: ^[a-z]+$
    state: present
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| custom_field | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
