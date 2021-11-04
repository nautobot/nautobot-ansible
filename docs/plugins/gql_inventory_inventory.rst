.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.networktocode.nautobot.gql_inventory_inventory:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.gql_inventory -- Nautobot inventory source using GraphQL capability
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.1.2).

    To install it use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.gql_inventory`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Get inventory hosts from Nautobot using GraphQL queries


.. Aliases


.. Requirements

Requirements
------------
The below requirements are needed on the local controller node that executes this inventory.

- netutils


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
                    <div class="ansibleOptionAnchor" id="parameter-additional_variables"></div>
                    <b>additional_variables</b>
                    <a class="ansibleOptionLink" href="#parameter-additional_variables" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">[]</div>
                                    </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Variable types and values to use while making the call</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-api_endpoint"></div>
                    <b>api_endpoint</b>
                    <a class="ansibleOptionLink" href="#parameter-api_endpoint" title="Permalink to this option"></a>
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
                                            <div>Endpoint of the Nautobot API</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-filters"></div>
                    <b>filters</b>
                    <a class="ansibleOptionLink" href="#parameter-filters" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">{}</div>
                                    </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Granular device search query</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-follow_redirects"></div>
                    <b>follow_redirects</b>
                    <a class="ansibleOptionLink" href="#parameter-follow_redirects" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>urllib2</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>all</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                                                                                                                                <li>safe</li>
                                                                                                                                                                                                <li>none</li>
                                                                                    </ul>
                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Determine how redirects are followed.</div>
                                            <div>By default, <em>follow_redirects</em> is set to uses urllib2 default behavior.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-group_by"></div>
                    <b>group_by</b>
                    <a class="ansibleOptionLink" href="#parameter-group_by" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>platform</li>
                                                                                                                                                                                                <li>status</li>
                                                                                                                                                                                                <li>device_role</li>
                                                                                                                                                                                                <li>site</li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">[]</div>
                                    </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>List of group names to group the hosts</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-plugin"></div>
                    <b>plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-plugin" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>networktocode.nautobot.gql_inventory</li>
                                                                                    </ul>
                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Setting that ensures this is a source file for the &#x27;networktocode.nautobot&#x27; plugin.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-query"></div>
                    <b>query</b>
                    <a class="ansibleOptionLink" href="#parameter-query" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">{}</div>
                                    </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>GraphQL query to send to Nautobot to obtain desired data</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-timeout"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">60</div>
                                    </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Timeout for Nautobot requests in seconds</div>
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
                                            <div>Nautobot API token to be able to read against Nautobot.</div>
                                            <div>This may not be required depending on the Nautobot setup.</div>
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
                                                                                            </td>
                                                <td>
                                            <div>Allows connection when SSL certificates are not valid. Set to <code>false</code> when certificates are not trusted.</div>
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

    
    # inventory.yml file in YAML format
    # Example command line: ansible-inventory -v --list -i inventory.yml

    # Add additional query parameter with query key
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    validate_certs: True
    query:
      tags: name

    # To group by use group_by key
    # Supported inputs are platform, status, device_role, site
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    validate_certs: True
    group_by:
      - platform

    # To group by use group_by key
    # Supported inputs are platform, status, device_role, site
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    validate_certs: True
    group_by:
      - platform


    # Add additional variables
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    validate_certs: True
    additional_variables:
      - device_role

    # Add additional variables combined with additional query
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    validate_certs: True
    query:
      interfaces: name
    additional_variables:
      - interfaces

    # Filter output using any supported parameters
    # To get supported parameters check the api/docs page for devices
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    validate_certs: True
    filters:
      name__ic: nym01-leaf-01
      site: nym01




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Armen Martirosyan



.. Parsing errors

