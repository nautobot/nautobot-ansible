.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.networktocode.nautobot.nautobot_server_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.nautobot_server -- Manages Nautobot Server application.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.0.0).

    To install it use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.nautobot_server`.

.. version_added

.. versionadded:: 3.0.0 of networktocode.nautobot

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manages Nautobot Server using the ``nautobot-server`` application frontend to ``django-admin``. With the ``virtualenv`` parameter, all management commands will be executed by the given ``virtualenv`` installation.


.. Aliases


.. Requirements

Requirements
------------
The below requirements are needed on the host that executes this module.

- nautobot


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
                    <div class="ansibleOptionAnchor" id="parameter-args"></div>
                    <b>args</b>
                    <a class="ansibleOptionLink" href="#parameter-args" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>A dictionary of the optional arguments and their values used together with the command.
    This translates {&quot;name_arg&quot;: &quot;value_arg&quot;} to &quot;--name_arg value_arg&quot;.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-command"></div>
                    <b>command</b>
                    <a class="ansibleOptionLink" href="#parameter-command" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The name of the Nautobot management command to run. Some command fully implemented are: <code>createsuperuser</code>,
    <code>migrate</code>, <code>makemigrations</code>, <code>post_upgrade</code> and <code>collectstatic</code>.
    Other commands can be entered, but will fail if they&#x27;re unknown to Nautobot or use positional arguments.
    The module will perform some basic parameter validation, when applicable, to the commands.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-db_password"></div>
                    <b>db_password</b>
                    <a class="ansibleOptionLink" href="#parameter-db_password" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Database password used in Nautobot.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-db_username"></div>
                    <b>db_username</b>
                    <a class="ansibleOptionLink" href="#parameter-db_username" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Database username used in Nautobot.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-flags"></div>
                    <b>flags</b>
                    <a class="ansibleOptionLink" href="#parameter-flags" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>A list of flags to append to the command that is passed to <code>nautobot-server</code>, so that [&quot;flag1&quot;, &quot;flag2&quot;] is translated to &quot;--flag1 --flag2&quot;.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-positional_args"></div>
                    <b>positional_args</b>
                    <a class="ansibleOptionLink" href="#parameter-positional_args" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>A list of additional arguments to append to the end of the command that is passed to <code>nautobot-server</code>.</div>
                                            <div>These are appended to the end of the command, so that [&quot;arg1&quot;, &quot;arg2&quot;] is translated to &quot;arg1 arg2&quot;.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-project_path"></div>
                    <b>project_path</b>
                    <a class="ansibleOptionLink" href="#parameter-project_path" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"/opt/nautobot"</div>
                                    </td>
                                                                <td>
                                            <div>The path to the root of the Nautobot application where <b>nautobot-server</b> lives.</div>
                                                                <div style="font-size: small; color: darkgreen"><br/>aliases: app_path, chdir</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-pythonpath"></div>
                    <b>pythonpath</b>
                    <a class="ansibleOptionLink" href="#parameter-pythonpath" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>A directory to add to the Python path. Typically used to include the settings module if it is located external to the application directory.</div>
                                                                <div style="font-size: small; color: darkgreen"><br/>aliases: python_path</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-settings"></div>
                    <b>settings</b>
                    <a class="ansibleOptionLink" href="#parameter-settings" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The Python path to the application&#x27;s settings module, such as &#x27;myapp.settings&#x27;.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-virtualenv"></div>
                    <b>virtualenv</b>
                    <a class="ansibleOptionLink" href="#parameter-virtualenv" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>An optional path to a <em>virtualenv</em> installation to use while running the nautobot-server application.</div>
                                                                <div style="font-size: small; color: darkgreen"><br/>aliases: virtual_env</div>
                                    </td>
            </tr>
                        </table>
    <br/>

.. Notes

Notes
-----

.. note::
   - This module is inspired from Django_manage Ansible module (https://github.com/ansible-collections/community.general/blob/main/plugins/modules/web_infrastructure/django_manage.py).
   - To be able to use the ``collectstatic`` command, you must have enabled staticfiles in your nautbot_config.py.
   - Your ``nautobot-server`` application must be executable (rwxr-xr-x), and must have a valid shebang, i.e. ``#!/usr/bin/env python``, for invoking the appropriate Python interpreter.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
      - name: Createsuperuser
        networktocode.nautobot.nautobot_server:
          command: "createsuperuser"
          args:
            email: "admin93@example.com"
            username: "superadmin7"
          db_password: "{{ db_password }}"
      - name: Collectstatic
        networktocode.nautobot.nautobot_server:
          command: "collectstatic"
          db_password: "{{ db_password }}"
      - name: Post Upgrade
        networktocode.nautobot.nautobot_server:
          command: "post_upgrade"
      - name: Make Migrations for Plugin
        networktocode.nautobot.nautobot_server:
          command: "makemigrations"
          positional_args: ["my_plugin_name"]
          db_password: "{{ db_password }}"
      - name: Migrate Plugin
        networktocode.nautobot.nautobot_server:
          command: "migrate"
          args:
            verbosity: 3
          flags: ["merge"]
          positional_args: ["my_plugin_name"]
          db_username: "{{ db_username }}"
          db_password: "{{ db_password }}"




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
                    <div class="ansibleOptionAnchor" id="return-changed"></div>
                    <b>changed</b>
                    <a class="ansibleOptionLink" href="#return-changed" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">boolean</span>
                                          </div>
                                    </td>
                <td>always</td>
                <td>
                                            <div>Boolean that is true if the command changed the state.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-cmd"></div>
                    <b>cmd</b>
                    <a class="ansibleOptionLink" href="#return-cmd" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>always</td>
                <td>
                                            <div>Full command executed in the Server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">nautobot-server createsuperuser --noinput --email=admin33@example.com --username=superadmin</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-out"></div>
                    <b>out</b>
                    <a class="ansibleOptionLink" href="#return-out" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>always</td>
                <td>
                                            <div>Raw output from the command execution.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">superadmin user already exists.</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-project_path"></div>
                    <b>project_path</b>
                    <a class="ansibleOptionLink" href="#return-project_path" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>always</td>
                <td>
                                            <div>The path to the root of the Nautobot application where <b>nautobot-server</b> lives.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/opt/nautobot</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Network to Code (@networktocode)



.. Parsing errors

