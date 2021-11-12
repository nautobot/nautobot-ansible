.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.lookup_graphql -- Queries and returns elements from Nautobot GraphQL endpoint
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.2.0).

    To install it use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.lookup_graphql`.

.. version_added

.. versionadded:: 1.1.0 of networktocode.nautobot

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Queries Nautobot via its GraphQL API through pynautobot


.. Aliases


.. Requirements

Requirements
------------
The below requirements are needed on the local controller node that executes this lookup.

- pynautobot


.. Options

Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                            <th>Configuration</th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-query"></div>
                    <b>query</b>
                    <a class="ansibleOptionLink" href="#parameter-query" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>The GraphQL formatted query string, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html).</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-token"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                            <div>
                                env:NAUTOBOT_TOKEN
                                                                                            </div>
                                                                    </td>
                                                <td>
                                            <div>The API token created through Nautobot</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-url"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-url" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                            <div>
                                env:NAUTOBOT_URL
                                                                                            </div>
                                                                    </td>
                                                <td>
                                            <div>The URL to the Nautobot instance to query (http://nautobot.example.com:8000)</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>
                    <b>validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">"yes"</div>
                                    </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Whether or not to validate SSL of the Nautobot instance</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-variables"></div>
                    <b>variables</b>
                    <a class="ansibleOptionLink" href="#parameter-variables" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Dictionary of keys/values to pass into the GraphQL query</div>
                                            <div>See [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details</div>
                                                        </td>
            </tr>
                        </table>
    <br/>

.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
      # Make API Query without variables
      - name: SET FACT OF STRING
        set_fact:
          query_string: |
            query {
              sites {
                id
                name
                region {
                  name
                }
              }
            }

      # Make query to GraphQL Endpoint
      - name: Obtain list of sites from Nautobot
        set_fact:
          query_response: "{{ query('networktocode.nautobot.lookup_graphql', query=query, url='https://nautobot.example.com', token='<redact>') }}"

      # Example with variables
      - name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
        set_fact:
          graph_variables:
            site_name: DEN
          query_string: |
            query ($site_name:String!) {
                sites (name: $site_name) {
                id
                name
                region {
                    name
                }
                }
            }

      # Get Response with variables
      - name: Obtain list of devices from Nautobot
        set_fact:
          query_response: "{{ query('networktocode.nautobot.lookup_graphql', query_string, graph_variables=graph_variables,
            url='https://nautobot.example.com', token='<redact>') }}"




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this lookup:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-data"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#return-data" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                                          </div>
                                    </td>
                <td>success</td>
                <td>
                                            <div>Data result from the GraphQL endpoint</div>
                                        <br/>
                                    </td>
            </tr>
                        </table>
    <br/><br/>

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Josh VanDeraa (@jvanderaa)



.. Parsing errors

