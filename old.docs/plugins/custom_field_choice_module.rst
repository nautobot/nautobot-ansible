.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.networktocode.nautobot.custom_field_choice_module:

.. Anchors: short name for ansible.builtin

.. Title

networktocode.nautobot.custom_field_choice module -- Creates or removes custom field choices from Nautobot
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/ui/repo/published/networktocode/nautobot/>`_ (version 5.3.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.networktocode.nautobot.custom_field_choice_module_requirements>` for details.

    To use it in a playbook, specify: :code:`networktocode.nautobot.custom_field_choice`.

.. version_added

.. rst-class:: ansible-version-added

New in networktocode.nautobot 5.1.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Creates or removes custom field choices from Nautobot


.. Aliases


.. Requirements

.. _ansible_collections.networktocode.nautobot.custom_field_choice_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- pynautobot






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_version"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-api_version:

      .. rst-class:: ansible-option-title

      **api_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in networktocode.nautobot 4.1.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      API Version Nautobot REST API


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-custom_field"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-custom_field:

      .. rst-class:: ansible-option-title

      **custom_field**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-custom_field" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.1.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Custom field this choice belongs to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query_params"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-query_params:

      .. rst-class:: ansible-option-title

      **query_params**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query_params" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This can be used to override the specified values in ALLOWED\_QUERY\_PARAMS that is defined

      in plugins/module\_utils/utils.py and provides control to users on what may make

      an object unique in their environment.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Use :literal:`present` or :literal:`absent` for adding or removing.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-token:

      .. rst-class:: ansible-option-title

      **token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The token created within Nautobot to authorize API access

      Can be omitted if the :ansenvvarref:`NAUTOBOT\_TOKEN` environment variable is configured.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-url"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-url:

      .. rst-class:: ansible-option-title

      **url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-url" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000)

      Can be omitted if the :ansenvvarref:`NAUTOBOT\_URL` environment variable is configured.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If :literal:`no`\ , SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.

      Can be omitted if the :ansenvvar:`NAUTOBOT\_VALIDATE\_CERTS` environment variable is configured.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`true`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-value"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-value" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.1.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Value of this choice


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-weight"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__parameter-weight:

      .. rst-class:: ansible-option-title

      **weight**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-weight" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.1.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Weight of this choice


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - This should be ran with connection :literal:`local` and hosts :literal:`localhost`

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    ---
    - name: Create a custom field choice
      networktocode.nautobot.custom_field_choice:
        url: http://nautobot.local
        token: thisIsMyToken
        value: "Choice 1"
        weight: 100
        custom_field: "Custom Field 1"
        state: present



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-custom_field_choice"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__return-custom_field_choice:

      .. rst-class:: ansible-option-title

      **custom_field_choice**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-custom_field_choice" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Serialized object as created or already existent within Nautobot


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success (when :emphasis:`state=present`\ )


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.networktocode.nautobot.custom_field_choice_module__return-msg:

      .. rst-class:: ansible-option-title

      **msg**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Message indicating failure or info about what has been achieved


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Joe Wesch (@joewesch)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/nautobot/nautobot-ansible/issues"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/nautobot/nautobot-ansible"
    external: true


.. Parsing errors
