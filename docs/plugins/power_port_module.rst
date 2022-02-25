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

.. _ansible_collections.networktocode.nautobot.power_port_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.power_port module -- Create, update or delete power ports within Nautobot
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.3.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.power_port`.

.. version_added

.. versionadded:: 1.0.0 of networktocode.nautobot

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Creates, updates or removes power ports from Nautobot


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
        <div class="ansibleOptionAnchor" id="parameter-allocated_draw"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-allocated_draw:

      .. rst-class:: ansible-option-title

      **allocated_draw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-allocated_draw" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The allocated draw of the power port in watt


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-description"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-description:

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

      Description of the power port


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-device"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-device:

      .. rst-class:: ansible-option-title

      **device**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-device" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`raw` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The device the power port is attached to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-maximum_draw"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-maximum_draw:

      .. rst-class:: ansible-option-title

      **maximum_draw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-maximum_draw" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The maximum permissible draw of the power port in watt


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the power port


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query_params"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-query_params:

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
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-state:

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
        <div class="ansibleOptionAnchor" id="parameter-tags"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-tags:

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

      Any tags that the power port may need to be associated with


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-token:

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

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-type" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The type of the power port


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`iec-60320-c6`
      - :ansible-option-choices-entry:`iec-60320-c8`
      - :ansible-option-choices-entry:`iec-60320-c14`
      - :ansible-option-choices-entry:`iec-60320-c16`
      - :ansible-option-choices-entry:`iec-60320-c20`
      - :ansible-option-choices-entry:`iec-60309-p-n-e-4h`
      - :ansible-option-choices-entry:`iec-60309-p-n-e-6h`
      - :ansible-option-choices-entry:`iec-60309-p-n-e-9h`
      - :ansible-option-choices-entry:`iec-60309-2p-e-4h`
      - :ansible-option-choices-entry:`iec-60309-2p-e-6h`
      - :ansible-option-choices-entry:`iec-60309-2p-e-9h`
      - :ansible-option-choices-entry:`iec-60309-3p-e-4h`
      - :ansible-option-choices-entry:`iec-60309-3p-e-6h`
      - :ansible-option-choices-entry:`iec-60309-3p-e-9h`
      - :ansible-option-choices-entry:`iec-60309-3p-n-e-4h`
      - :ansible-option-choices-entry:`iec-60309-3p-n-e-6h`
      - :ansible-option-choices-entry:`iec-60309-3p-n-e-9h`
      - :ansible-option-choices-entry:`nema-5-15p`
      - :ansible-option-choices-entry:`nema-5-20p`
      - :ansible-option-choices-entry:`nema-5-30p`
      - :ansible-option-choices-entry:`nema-5-50p`
      - :ansible-option-choices-entry:`nema-6-15p`
      - :ansible-option-choices-entry:`nema-6-20p`
      - :ansible-option-choices-entry:`nema-6-30p`
      - :ansible-option-choices-entry:`nema-6-50p`
      - :ansible-option-choices-entry:`nema-l5-15p`
      - :ansible-option-choices-entry:`nema-l5-20p`
      - :ansible-option-choices-entry:`nema-l5-30p`
      - :ansible-option-choices-entry:`nema-l5-50p`
      - :ansible-option-choices-entry:`nema-l6-20p`
      - :ansible-option-choices-entry:`nema-l6-30p`
      - :ansible-option-choices-entry:`nema-l6-50p`
      - :ansible-option-choices-entry:`nema-l14-20p`
      - :ansible-option-choices-entry:`nema-l14-30p`
      - :ansible-option-choices-entry:`nema-l21-20p`
      - :ansible-option-choices-entry:`nema-l21-30p`
      - :ansible-option-choices-entry:`cs6361c`
      - :ansible-option-choices-entry:`cs6365c`
      - :ansible-option-choices-entry:`cs8165c`
      - :ansible-option-choices-entry:`cs8265c`
      - :ansible-option-choices-entry:`cs8365c`
      - :ansible-option-choices-entry:`cs8465c`
      - :ansible-option-choices-entry:`ita-e`
      - :ansible-option-choices-entry:`ita-f`
      - :ansible-option-choices-entry:`ita-ef`
      - :ansible-option-choices-entry:`ita-g`
      - :ansible-option-choices-entry:`ita-h`
      - :ansible-option-choices-entry:`ita-i`
      - :ansible-option-choices-entry:`ita-j`
      - :ansible-option-choices-entry:`ita-k`
      - :ansible-option-choices-entry:`ita-l`
      - :ansible-option-choices-entry:`ita-m`
      - :ansible-option-choices-entry:`ita-n`
      - :ansible-option-choices-entry:`ita-o`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-url"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-url:

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

      .. _ansible_collections.networktocode.nautobot.power_port_module__parameter-validate_certs:

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

    
    - name: "Test Nautobot modules"
      connection: local
      hosts: localhost
      gather_facts: False

      tasks:
        - name: Create power port within Nautobot with only required information
          networktocode.nautobot.power_port:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Test Power Port
            device: Test Device
            state: present

        - name: Update power port with other fields
          networktocode.nautobot.power_port:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Test Power Port
            device: Test Device
            type: iec-60320-c6
            allocated_draw: 16
            maximum_draw: 80
            description: power port description
            state: present

        - name: Delete power port within nautobot
          networktocode.nautobot.power_port:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Test Power Port
            device: Test Device
            state: absent




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

      .. _ansible_collections.networktocode.nautobot.power_port_module__return-msg:

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
        <div class="ansibleOptionAnchor" id="return-power_port"></div>

      .. _ansible_collections.networktocode.nautobot.power_port_module__return-power_port:

      .. rst-class:: ansible-option-title

      **power_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-power_port" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Serialized object as created or already existent within Nautobot


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success (when \ :emphasis:`state=present`\ )


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Tobias Groß (@toerb)



.. Parsing errors

