
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

.. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.ip_address_to_interface module -- Creates or removes IP address to interface association from Nautobot
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 5.2.0).

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.networktocode.nautobot.ip_address_to_interface_module_requirements>` for details.

    To use it in a playbook, specify: :code:`networktocode.nautobot.ip_address_to_interface`.

.. version_added

.. rst-class:: ansible-version-added

New in networktocode.nautobot 5.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Creates or removes IP address to interface association from Nautobot


.. Aliases


.. Requirements

.. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module_requirements:

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

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-api_version:

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
        <div class="ansibleOptionAnchor" id="parameter-interface"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-interface:

      .. rst-class:: ansible-option-title

      **interface**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-interface" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Device interface to associate with an IP.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ip_address"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-ip_address:

      .. rst-class:: ansible-option-title

      **ip_address**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ip_address" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      IP address to associate with an interface.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query_params"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-query_params:

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
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-state:

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

      Use \ :literal:`present`\  or \ :literal:`absent`\  for adding, or removing.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-token:

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

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-url:

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

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-validate_certs:

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
        <div class="ansibleOptionAnchor" id="parameter-vm_interface"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__parameter-vm_interface:

      .. rst-class:: ansible-option-title

      **vm_interface**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vm_interface" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in networktocode.nautobot 5.0.0`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      VM interface to associate with an IP.


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

    
    - name: "Test Nautobot IP address to interface module"
      connection: local
      hosts: localhost
      gather_facts: False

      tasks:
        - name: "Add IP address on GigabitEthernet4 - test100"
          networktocode.nautobot.ip_address_to_interface:
            url: "{{ nautobot_url }}"
            token: "{{ nautobot_token }}"
            ip_address: "{{ ip_address['key'] }}"
            interface:
              name: GigabitEthernet4
              device: test100
          vars:
            ip_address: "{{ lookup('networktocode.nautobot.lookup', 'ip-addresses', api_endpoint=nautobot_url, token=nautobot_token, api_filter='address=10.100.0.1/32') }}"

        - name: "Delete IP address on GigabitEthernet4 - test100"
          networktocode.nautobot.ip_address_to_interface:
            url: "{{ nautobot_url }}"
            token: "{{ nautobot_token }}"
            ip_address: "{{ ip_address['key'] }}"
            interface:
              name: GigabitEthernet4
              device: test100
            state: absent
          vars:
            ip_address: "{{ lookup('networktocode.nautobot.lookup', 'ip-addresses', api_endpoint=nautobot_url, token=nautobot_token, api_filter='address=10.100.0.1/32') }}"





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
        <div class="ansibleOptionAnchor" id="return-ip_address_to_interface"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__return-ip_address_to_interface:

      .. rst-class:: ansible-option-title

      **ip_address_to_interface**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-ip_address_to_interface" title="Permalink to this return value"></a>

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


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.networktocode.nautobot.ip_address_to_interface_module__return-msg:

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

