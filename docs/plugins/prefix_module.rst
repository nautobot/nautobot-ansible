
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

.. _ansible_collections.networktocode.nautobot.prefix_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.prefix module -- Creates or removes prefixes from Nautobot
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 5.0.1).

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.networktocode.nautobot.prefix_module_requirements>` for details.

    To use it in a playbook, specify: :code:`networktocode.nautobot.prefix`.

.. version_added

.. rst-class:: ansible-version-added

New in networktocode.nautobot 1.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Creates or removes prefixes from Nautobot


.. Aliases


.. Requirements

.. _ansible_collections.networktocode.nautobot.prefix_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- pynautobot






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
        <div class="ansibleOptionAnchor" id="parameter-api_version"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-api_version:

      .. rst-class:: ansible-option-title

      **api_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_version" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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
        <div class="ansibleOptionAnchor" id="parameter-custom_fields"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-custom_fields:

      .. rst-class:: ansible-option-title

      **custom_fields**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-custom_fields" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Must exist in Nautobot and in key/value format


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-description"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-description:

      .. rst-class:: ansible-option-title

      **description**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-description" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The description of the prefix


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-first_available"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-first_available:

      .. rst-class:: ansible-option-title

      **first_available**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-first_available" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If \ :literal:`yes`\  and state \ :literal:`present`\ , if an parent is given, it will get the first available prefix of the given prefix\_length inside the given parent (and namespace, if given). Unused with state \ :literal:`absent`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ip_version"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-ip_version:

      .. rst-class:: ansible-option-title

      **ip_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ip_version" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Specifies which address version the prefix prefix belongs to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-location"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-location:

      .. rst-class:: ansible-option-title

      **location**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-location" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Location that prefix is associated with


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-namespace"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-namespace:

      .. rst-class:: ansible-option-title

      **namespace**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-namespace" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      namespace that IP address is associated with. IPs are unique per namespaces.
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Global"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-parent"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-parent:

      .. rst-class:: ansible-option-title

      **parent**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-parent" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if state is \ :literal:`present`\  and first\_available is \ :literal:`yes`\ . Will get a new available prefix in this parent prefix.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-prefix"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-prefix:

      .. rst-class:: ansible-option-title

      **prefix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-prefix" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if state is \ :literal:`present`\  and first\_available is False. Will allocate or free this prefix.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-prefix_length"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-prefix_length:

      .. rst-class:: ansible-option-title

      **prefix_length**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-prefix_length" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required ONLY if state is \ :literal:`present`\  and first\_available is \ :literal:`yes`\ .
          Will get a new available prefix of the given prefix\_length in this parent prefix.
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query_params"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-query_params:

      .. rst-class:: ansible-option-title

      **query_params**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query_params" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

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
        <div class="ansibleOptionAnchor" id="parameter-role"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-role:

      .. rst-class:: ansible-option-title

      **role**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-role" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The role of the prefix


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Use \ :literal:`present`\  or \ :literal:`absent`\  for adding or removing.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-status"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-status:

      .. rst-class:: ansible-option-title

      **status**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-status" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The status of the prefix

      Required if \ :emphasis:`state=present`\  and does not exist yet


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-tags"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-tags:

      .. rst-class:: ansible-option-title

      **tags**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-tags" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Any tags that this item may need to be associated with


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-tenant"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-tenant:

      .. rst-class:: ansible-option-title

      **tenant**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-tenant" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The tenant that the prefix will be assigned to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-token:

      .. rst-class:: ansible-option-title

      **token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The token created within Nautobot to authorize API access


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-type"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-type" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Prefix type


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Container"`
      - :ansible-option-choices-entry:`"Network"`
      - :ansible-option-choices-entry:`"Pool"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-url"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-url:

      .. rst-class:: ansible-option-title

      **url**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-url" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If \ :literal:`no`\ , SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`true`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vlan"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-vlan:

      .. rst-class:: ansible-option-title

      **vlan**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vlan" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 3.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The VLAN the prefix will be assigned to


      .. raw:: html

        </div>


.. Attributes


.. Notes

Notes
-----

.. note::
   - Tags should be defined as a YAML list
   - This should be ran with connection \ :literal:`local`\  and hosts \ :literal:`localhost`\ 

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: "Test Nautobot prefix module"
      connection: local
      hosts: localhost
      gather_facts: False

      tasks:
        - name: Create prefix within Nautobot with only required information
          networktocode.nautobot.prefix:
            url: http://nautobot.local
            token: thisIsMyToken
            prefix: 10.156.0.0/19
            status: active
            state: present

        - name: Delete prefix within nautobot
          networktocode.nautobot.prefix:
            url: http://nautobot.local
            token: thisIsMyToken
            prefix: 10.156.0.0/19
            state: absent

        - name: Create prefix with several specified options
          networktocode.nautobot.prefix:
            url: http://nautobot.local
            token: thisIsMyToken
            family: 4
            prefix: 10.156.32.0/19
            location: Test Location
            tenant: Test Tenant
            vlan:
              name: Test VLAN
              location: Test Location
              tenant: Test Tenant
              vlan_group: Test Vlan Group
            status: Reserved
            role: Network of care
            description: Test description
            type: Pool
            tags:
              - Schnozzberry
            state: present

        - name: Get a new /24 inside 10.156.0.0/19 within Nautobot - Parent doesn't exist
          networktocode.nautobot.prefix:
            url: http://nautobot.local
            token: thisIsMyToken
            parent: 10.156.0.0/19
            prefix_length: 24
            state: present
            first_available: yes

        - name: Create prefix within Nautobot with only required information
          networktocode.nautobot.prefix:
            url: http://nautobot.local
            token: thisIsMyToken
            prefix: 10.156.0.0/19
            state: present

        - name: Get a new /24 inside 10.156.0.0/19 within Nautobot
          networktocode.nautobot.prefix:
            url: http://nautobot.local
            token: thisIsMyToken
            parent: 10.156.0.0/19
            prefix_length: 24
            state: present
            first_available: yes

        - name: Get a new /24 inside 10.157.0.0/19 within Nautobot with additional values
          networktocode.nautobot.prefix:
            url: http://nautobot.local
            token: thisIsMyToken
            parent: 10.157.0.0/19
            prefix_length: 24
            location: Test Location
            state: present
            first_available: yes




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
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__return-msg:

      .. rst-class:: ansible-option-title

      **msg**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

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


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-prefix"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__return-prefix:

      .. rst-class:: ansible-option-title

      **prefix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-prefix" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Serialized object as created or already existent within Nautobot


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` on creation


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Mikhail Yohman (@FragmentedPacket)
- Anthony Ruhier (@Anthony25)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/nautobot/nautobot-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/nautobot/nautobot-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

