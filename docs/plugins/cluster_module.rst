.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.networktocode.nautobot.cluster_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.cluster -- Create, update or delete clusters within Nautobot
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.0.0).

    To install it use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.cluster`.

.. version_added

.. versionadded:: 1.0.0 of networktocode.nautobot

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Creates, updates or removes clusters from Nautobot


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
                    <div class="ansibleOptionAnchor" id="parameter-cluster_group"></div>
                    <b>cluster_group</b>
                    <a class="ansibleOptionLink" href="#parameter-cluster_group" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>group of the cluster</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-cluster_type"></div>
                    <b>cluster_type</b>
                    <a class="ansibleOptionLink" href="#parameter-cluster_type" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>type of the cluster</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-comments"></div>
                    <b>comments</b>
                    <a class="ansibleOptionLink" href="#parameter-comments" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Comments that may include additional information in regards to the cluster</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-custom_fields"></div>
                    <b>custom_fields</b>
                    <a class="ansibleOptionLink" href="#parameter-custom_fields" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>must exist in Nautobot</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-name"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The name of the cluster</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-query_params"></div>
                    <b>query_params</b>
                    <a class="ansibleOptionLink" href="#parameter-query_params" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined</div>
                                            <div>in plugins/module_utils/utils.py and provides control to users on what may make</div>
                                            <div>an object unique in their environment.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-site"></div>
                    <b>site</b>
                    <a class="ansibleOptionLink" href="#parameter-site" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Required if <em>state=present</em> and the cluster does not exist yet</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-state"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Use <code>present</code> or <code>absent</code> for adding or removing.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-tags"></div>
                    <b>tags</b>
                    <a class="ansibleOptionLink" href="#parameter-tags" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=raw</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Any tags that the cluster may need to be associated with</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-tenant"></div>
                    <b>tenant</b>
                    <a class="ansibleOptionLink" href="#parameter-tenant" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Tenant the cluster will be assigned to.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-token"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The token created within Nautobot to authorize API access</div>
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
                                            <div>URL of the Nautobot instance resolvable by Ansible control host</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>
                    <b>validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">"yes"</div>
                                    </td>
                                                                <td>
                                            <div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div>
                                                        </td>
            </tr>
                        </table>
    <br/>

.. Notes

Notes
-----

.. note::
   - Tags should be defined as a YAML list
   - This should be ran with connection ``local`` and hosts ``localhost``

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
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

        - name: Update the group and site of an existing cluster
          networktocode.nautobot.cluster:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Test Cluster
            cluster_type: qemu
            cluster_group: GROUP
            site: SITE
            state: present




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
                    <div class="ansibleOptionAnchor" id="return-cluster"></div>
                    <b>cluster</b>
                    <a class="ansibleOptionLink" href="#return-cluster" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                                          </div>
                                    </td>
                <td>success (when <em>state=present</em>)</td>
                <td>
                                            <div>Serialized object as created or already existent within Nautobot</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-msg"></div>
                    <b>msg</b>
                    <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>always</td>
                <td>
                                            <div>Message indicating failure or info about what has been achieved</div>
                                        <br/>
                                    </td>
            </tr>
                        </table>
    <br/><br/>

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Gaelle MANGIN (@gmangin)



.. Parsing errors

