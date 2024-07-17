# networktocode.nautobot.query_graphql

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.query_graphql`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- No synopsis available.

## Requirements

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str |  | API Version Nautobot REST API |
| graph_variables | dict |  | Dictionary of keys/values to pass into the GraphQL query, see (U(https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html)) for more info |
| query | str |  | The GraphQL formatted query string, see (U(https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html)) for more details. |
| token | str |  | The API token created through Nautobot, optional env=NAUTOBOT_TOKEN |
| update_hostvars | bool |  | Whether or not to populate data in the in the root (e.g. hostvars[inventory_hostname]) or within the 'data' key (e.g. hostvars[inventory_hostname]['data']). Beware, that the root keys provided by the query will overwrite any root keys already present, leverage the GraphQL alias feature to avoid issues. |
| url | str |  | The URL to the Nautobot instance to query (http://nautobot.example.com:8000), optional env=NAUTOBOT_URL |
| validate_certs | bool |  | Whether or not to validate SSL of the Nautobot instance |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
# Make API Query without variables
  - name: SET FACT OF STRING
    set_fact:
      query_string: |
        query {
          locations {
            id
            name
            parent {
              name
            }
          }
        }

  # Make query to GraphQL Endpoint
  - name: Obtain list of locations from Nautobot
    networktocode.nautobot.query_graphql:
      url: http://nautobot.local
      token: thisIsMyToken
      query: "{{ query_string }}"


  # Example with variables
  - name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
    set_fact:
      graph_variables:
        $location_name: AMS01
      query_string: |
        query ($location_name: String!) {
          locations (name: $location_name) {
            id
            name
            parent {
                name
            }
          }
        }

  # Get Response with variables and set to root keys
  - name: Obtain list of devices at location in variables from Nautobot
    networktocode.nautobot.query_graphql:
      url: http://nautobot.local
      token: thisIsMyToken
      query: "{{ query_string }}"
      graph_variables: "{{ graph_variables }}"
      update_hostvars: yes
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
