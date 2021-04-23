.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.networktocode.nautobot.lookup_lookup:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.lookup -- Queries and returns elements from Nautobot
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 1.0.4).

    To install it use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.lookup`.

.. version_added

.. versionadded:: 1.0.0 of networktocode.nautobot

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Queries Nautobot via its API to return virtually any information capable of being held in Nautobot.


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
                    <div class="ansibleOptionAnchor" id="parameter-_terms"></div>
                    <b>_terms</b>
                    <a class="ansibleOptionLink" href="#parameter-_terms" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>The Nautobot object type to query</div>
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
                                            <div>The URL to the Nautobot instance to query</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-api_filter"></div>
                    <b>api_filter</b>
                    <a class="ansibleOptionLink" href="#parameter-api_filter" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>The api_filter to use.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-plugin"></div>
                    <b>plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-plugin" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>The Nautobot plugin to query</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-raw_data"></div>
                    <b>raw_data</b>
                    <a class="ansibleOptionLink" href="#parameter-raw_data" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Whether to return raw API data with the lookup/query or whether to return a key/value dict</div>
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
                                            <div>This may not be required depending on the Nautobot setup.</div>
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
                        </table>
    <br/>

.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    tasks:
      # query a list of devices
      - name: Obtain list of devices from Nautobot
        debug:
          msg: >
            "Device {{ item.value.display }} (ID: {{ item.key }}) was
             manufactured by {{ item.value.device_type.manufacturer.name }}"
        loop: "{{ query('networktocode.nautobot.lookup', 'devices',
                        api_endpoint='http://localhost/',
                        token='<redacted>') }}"

    # This example uses an API Filter
    tasks:
      # query a list of devices
      - name: Obtain list of devices from Nautobot
        debug:
          msg: >
            "Device {{ item.value.display }} (ID: {{ item.key }}) was
             manufactured by {{ item.value.device_type.manufacturer.name }}"
        loop: "{{ query('networktocode.nautobot.lookup', 'devices',
                        api_endpoint='http://localhost/',
                        api_filter='role=management tag=Dell'),
                        token='<redacted>') }}"

    # Fetch bgp sessions for R1-device
    tasks:
      - name: "Obtain bgp sessions for R1-Device"
        debug:
          msg: "{{ query('networktocode.nautobot.lookup', 'bgp_sessions',
                         api_filter='device=R1-Device',
                         api_endpoint='http://localhost/',
                         token='<redacted>',
                         plugin='mycustomstuff') }}"




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
                    <div class="ansibleOptionAnchor" id="return-_list"></div>
                    <b>_list</b>
                    <a class="ansibleOptionLink" href="#return-_list" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>success</td>
                <td>
                                            <div>list of composed dictionaries with key and value</div>
                                        <br/>
                                    </td>
            </tr>
                        </table>
    <br/><br/>

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Chris Mills (@cpmills1975)



.. Parsing errors

