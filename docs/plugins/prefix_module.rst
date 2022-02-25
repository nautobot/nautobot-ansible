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
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
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
    This module is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.3.1).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.prefix`.

.. version_added

.. versionadded:: 1.0.0 of networktocode.nautobot

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
        <div class="ansibleOptionAnchor" id="parameter-custom_fields"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-custom_fields:

      .. rst-class:: ansible-option-title

      **custom_fields**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-custom_fields" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


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

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The description of the prefix


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-family"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-family:

      .. rst-class:: ansible-option-title

      **family**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-family" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Specifies which address family the prefix prefix belongs to


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

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If \ :literal:`yes`\  and state \ :literal:`present`\ , if an parent is given, it will get the first available prefix of the given prefix_length inside the given parent (and vrf, if given). Unused with state \ :literal:`absent`\ .


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-is_pool"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-is_pool:

      .. rst-class:: ansible-option-title

      **is_pool**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-is_pool" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      All IP Addresses within this prefix are considered usable


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-choices-entry:`yes`

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

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if state is \ :literal:`present`\  and first_available is \ :literal:`yes`\ . Will get a new available prefix in this parent prefix.


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

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if state is \ :literal:`present`\  and first_available is False. Will allocate or free this prefix.


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

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required ONLY if state is \ :literal:`present`\  and first_available is \ :literal:`yes`\ .
          Will get a new available prefix of the given prefix_length in this parent prefix.
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-prefix_role"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-prefix_role:

      .. rst-class:: ansible-option-title

      **prefix_role**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-prefix_role" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The role of the prefix


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

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined

      in plugins/module_utils/utils.py and provides control to users on what may make

      an object unique in their environment.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Site that prefix is associated with


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

      - :ansible-option-choices-entry:`absent`
      - :ansible-option-default-bold:`present` :ansible-option-default:`← (default)`

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

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


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

      :ansible-option-type:`list` / :ansible-option-elements:`elements=raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Any tags that the prefix may need to be associated with


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

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


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

      URL of the Nautobot instance resolvable by Ansible control host


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

      :ansible-option-type:`raw`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If \ :literal:`no`\ , SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"yes"`

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

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The VLAN the prefix will be assigned to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vrf"></div>

      .. _ansible_collections.networktocode.nautobot.prefix_module__parameter-vrf:

      .. rst-class:: ansible-option-title

      **vrf**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vrf" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`raw`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      VRF that prefix is associated with


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
            site: Test Site
            vrf: Test VRF
            tenant: Test Tenant
            vlan:
              name: Test VLAN
              site: Test Site
              tenant: Test Tenant
              vlan_group: Test Vlan Group
            status: Reserved
            prefix_role: Network of care
            description: Test description
            is_pool: true
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
            vrf: Test VRF
            site: Test Site
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



.. Parsing errors

