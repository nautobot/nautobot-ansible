
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.networktocode.nautobot.nautobot_server_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.nautobot_server module -- Manages Nautobot Server application.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 5.0.0).

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.networktocode.nautobot.nautobot_server_module_requirements>` for details.

    To use it in a playbook, specify: :code:`networktocode.nautobot.nautobot_server`.

.. version_added

.. rst-class:: ansible-version-added

New in networktocode.nautobot 3.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manages Nautobot Server using the \ :literal:`nautobot-server`\  application frontend to \ :literal:`django-admin`\ . With the \ :literal:`virtualenv`\  parameter
- all management commands will be executed by the given \ :literal:`virtualenv`\  installation.


.. Aliases


.. Requirements

.. _ansible_collections.networktocode.nautobot.nautobot_server_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- nautobot






.. Options

Parameters
----------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-args"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-args:

      .. rst-class:: ansible-option-title

      **args**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-args" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A dictionary of the optional arguments and their values used together with the command.
          This translates {"name\_arg": "value\_arg"} to "--name\_arg value\_arg".
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-command"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-command:

      .. rst-class:: ansible-option-title

      **command**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-command" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the Nautobot management command to run. Some command fully implemented are: \ :literal:`createsuperuser`\ ,
          \ :literal:`migrate`\ , \ :literal:`makemigrations`\ , \ :literal:`post\_upgrade`\  and \ :literal:`collectstatic`\ .
          Other commands can be entered, but will fail if they're unknown to Nautobot or use positional arguments.
          The module will perform some basic parameter validation, when applicable, to the commands.
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-db_password"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-db_password:

      .. rst-class:: ansible-option-title

      **db_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-db_password" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Database password used in Nautobot.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-db_username"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-db_username:

      .. rst-class:: ansible-option-title

      **db_username**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-db_username" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Database username used in Nautobot.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-flags"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-flags:

      .. rst-class:: ansible-option-title

      **flags**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-flags" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of flags to append to the command that is passed to \ :literal:`nautobot-server`\ , so that ["flag1", "flag2"] is translated to "--flag1 --flag2".


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-positional_args"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-positional_args:

      .. rst-class:: ansible-option-title

      **positional_args**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-positional_args" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of additional arguments to append to the end of the command that is passed to \ :literal:`nautobot-server`\ .

      These are appended to the end of the command, so that ["arg1", "arg2"] is translated to "arg1 arg2".


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-project_path"></div>
        <div class="ansibleOptionAnchor" id="parameter-app_path"></div>
        <div class="ansibleOptionAnchor" id="parameter-chdir"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-app_path:
      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-chdir:
      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-project_path:

      .. rst-class:: ansible-option-title

      **project_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-project_path" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: app_path, chdir`

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to the root of the Nautobot application where \ :strong:`nautobot-server`\  lives.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"/opt/nautobot"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-pythonpath"></div>
        <div class="ansibleOptionAnchor" id="parameter-python_path"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-python_path:
      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-pythonpath:

      .. rst-class:: ansible-option-title

      **pythonpath**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-pythonpath" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: python_path`

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A directory to add to the Python path. Typically used to include the settings module if it is located external to the application directory.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-settings"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-settings:

      .. rst-class:: ansible-option-title

      **settings**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-settings" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Python path to the application's settings module, such as 'myapp.settings'.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-virtualenv"></div>
        <div class="ansibleOptionAnchor" id="parameter-virtual_env"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-virtual_env:
      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__parameter-virtualenv:

      .. rst-class:: ansible-option-title

      **virtualenv**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-virtualenv" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-aliases:`aliases: virtual_env`

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      An optional path to a \ :emphasis:`virtualenv`\  installation to use while running the nautobot-server application.


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - Inspired from Django\_manage (\ https://github.com/ansible-collections/community.general/blob/main/plugins/modules/web_infrastructure/django_manage.py\ ).
   - To be able to use the \ :literal:`collectstatic`\  command, you must have enabled staticfiles in your nautbot\_config.py.
   - Your \ :literal:`nautobot-server`\  application must be executable (rwxr-xr-x), and must have a valid shebang.

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

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-changed"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__return-changed:

      .. rst-class:: ansible-option-title

      **changed**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-changed" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Boolean that is true if the command changed the state.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`true`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-cmd"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__return-cmd:

      .. rst-class:: ansible-option-title

      **cmd**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-cmd" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Full command executed in the Server.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"nautobot-server createsuperuser --noinput --email=admin33@example.com --username=superadmin"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-out"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__return-out:

      .. rst-class:: ansible-option-title

      **out**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-out" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Raw output from the command execution.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"superadmin user already exists."`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-project_path"></div>

      .. _ansible_collections.networktocode.nautobot.nautobot_server_module__return-project_path:

      .. rst-class:: ansible-option-title

      **project_path**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-project_path" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The path to the root of the Nautobot application where \ :strong:`nautobot-server`\  lives.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"/opt/nautobot"`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Network to Code (@networktocode)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/nautobot/nautobot-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/nautobot/nautobot-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

