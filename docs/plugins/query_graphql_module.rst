.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.networktocode.nautobot.query_graphql_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.query_graphql -- Queries and returns elements from Nautobot GraphQL endpoint
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.2.1).

    To install it use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.query_graphql`.

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

.. note::
    This module has a corresponding :ref:`action plugin <action_plugins>`.

.. Aliases


.. Requirements

Requirements
------------
The below requirements are needed on the host that executes this module.

- pynautobot


.. Options

Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-graph_variables"></div>
                    <b>graph_variables</b>
                    <a class="ansibleOptionLink" href="#parameter-graph_variables" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Dictionary of keys/values to pass into the GraphQL query, see (<a href='https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html'>https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html</a>) for more info</div>
                                                        </td>
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
                                            <div>The GraphQL formatted query string, see (<a href='https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html'>https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html</a>) for more details.</div>
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
                                            <div>The API token created through Nautobot, optional env=NAUTOBOT_TOKEN</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-update_hostvars"></div>
                    <b>update_hostvars</b>
                    <a class="ansibleOptionLink" href="#parameter-update_hostvars" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Whether or not to populate data in the in the root (e.g. hostvars[inventory_hostname]) or within the &#x27;data&#x27; key (e.g. hostvars[inventory_hostname][&#x27;data&#x27;]). Beware, that the root keys provided by the query will overwrite any root keys already present, leverage the GraphQL alias feature to avoid issues.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-url"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-url" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The URL to the Nautobot instance to query (http://nautobot.example.com:8000), optional env=NAUTOBOT_URL</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>
                    <b>validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Whether or not to validate SSL of the Nautobot instance</div>
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
        networktocode.nautobot.query_graphql:
          url: http://nautobot.local
          token: thisIsMyToken
          query: "{{ query_string }}"


      # Example with variables
      - name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
        set_fact:
          variables:
            site_name: den
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

      # Get Response with variables and set to root keys
      - name: Obtain list of devices at site in variables from Nautobot
        networktocode.nautobot.query_graphql:
          url: http://nautobot.local
          token: thisIsMyToken
          query: "{{ query_string }}"
          variables: "{{ variables }}"
          update_hostvars: "yes"




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

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
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-graph_variables"></div>
                    <b>graph_variables</b>
                    <a class="ansibleOptionLink" href="#return-graph_variables" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                                          </div>
                                    </td>
                <td>success</td>
                <td>
                                            <div>Variables passed in</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-query"></div>
                    <b>query</b>
                    <a class="ansibleOptionLink" href="#return-query" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>success</td>
                <td>
                                            <div>Query string that was sent to Nautobot</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-url"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#return-url" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>success</td>
                <td>
                                            <div>Nautobot URL that was supplied for troubleshooting</div>
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

