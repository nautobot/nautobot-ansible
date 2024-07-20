# networktocode.nautobot.lookup_graphql

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module, see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.lookup_graphql`.

## Synopsis

- Queries Nautobot via its GraphQL API through pynautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Environment Variable | Version Added | Comments |
| --------- | --------- | -------------------- | ------------- | -------- |
| api_version |  |  | 4.1.0 | The Nautobot Rest API Version to use |
| graph_variables |  |  |  | Dictionary of keys/values to pass into the GraphQL query See [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details |
| query |  |  |  | The GraphQL formatted query string, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html). |
| token |  |  NAUTOBOT_TOKEN  |  | The API token created through Nautobot |
| url |  |  NAUTOBOT_URL  |  | The URL to the Nautobot instance to query (http://nautobot.example.com:8000) |
| validate_certs |  |  |  | Whether or not to validate SSL of the Nautobot instance |


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
    set_fact:
      query_response: "{{ query('networktocode.nautobot.lookup_graphql', query=query_string, url='https://nautobot.example.com', token='<redact>') }}"

  # Example with variables
  - name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
    set_fact:
      graph_variables:
        location_name: DEN
      query_string: |
        query ($location_name:String!) {
            locations (name: $location_name) {
            id
            name
            parent {
                name
            }
            }
        }

  # Get Response with variables
  - name: Obtain list of devices from Nautobot
    set_fact:
      query_response: "{{ query('networktocode.nautobot.lookup_graphql', query_string, graph_variables=graph_variables,
        url='https://nautobot.example.com', token='<redact>') }}"

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| data | dict | Data result from the GraphQL endpoint |  |

## Authors

- Josh VanDeraa (@jvanderaa)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
