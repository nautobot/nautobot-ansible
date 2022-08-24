
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

.. _ansible_collections.networktocode.nautobot.device_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.device module -- Create, update or delete devices within Nautobot
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 4.1.0).

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.networktocode.nautobot.device_module_requirements>` for details.

    To use it in a playbook, specify: :code:`networktocode.nautobot.device`.

.. version_added

.. versionadded:: 1.0.0 of networktocode.nautobot

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Creates, updates or removes devices from Nautobot


.. Aliases


.. Requirements

.. _ansible_collections.networktocode.nautobot.device_module_requirements:

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

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-api_version:

      .. rst-class:: ansible-option-title

      **api_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_version" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in 4.1.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      API Version Nautobot REST API


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-asset_tag"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-asset_tag:

      .. rst-class:: ansible-option-title

      **asset_tag**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-asset_tag" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Asset tag that is associated to the device


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cluster"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-cluster:

      .. rst-class:: ansible-option-title

      **cluster**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cluster" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Cluster that the device will be assigned to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-comments"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-comments:

      .. rst-class:: ansible-option-title

      **comments**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-comments" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Comments that may include additional information in regards to the device


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-custom_fields"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-custom_fields:

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

      must exist in Nautobot


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-device_role"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-device_role:

      .. rst-class:: ansible-option-title

      **device_role**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-device_role" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if \ :emphasis:`state=present`\  and the device does not exist yet


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-device_type"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-device_type:

      .. rst-class:: ansible-option-title

      **device_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-device_type" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if \ :emphasis:`state=present`\  and the device does not exist yet


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-face"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-face:

      .. rst-class:: ansible-option-title

      **face**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-face" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if \ :emphasis:`rack`\  is defined


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`Front`
      - :ansible-option-choices-entry:`front`
      - :ansible-option-choices-entry:`Rear`
      - :ansible-option-choices-entry:`rear`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-local_context_data"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-local_context_data:

      .. rst-class:: ansible-option-title

      **local_context_data**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-local_context_data" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Arbitrary JSON data to define the devices configuration variables.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-name:

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

      The name of the device


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-platform"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-platform:

      .. rst-class:: ansible-option-title

      **platform**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-platform" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The platform of the device


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-position"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-position:

      .. rst-class:: ansible-option-title

      **position**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-position" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The position of the device in the rack defined above


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-primary_ip4"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-primary_ip4:

      .. rst-class:: ansible-option-title

      **primary_ip4**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-primary_ip4" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Primary IPv4 address assigned to the device


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-primary_ip6"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-primary_ip6:

      .. rst-class:: ansible-option-title

      **primary_ip6**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-primary_ip6" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Primary IPv6 address assigned to the device


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query_params"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-query_params:

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

      This can be used to override the specified values in ALLOWED\_QUERY\_PARAMS that is defined

      in plugins/module\_utils/utils.py and provides control to users on what may make

      an object unique in their environment.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-rack"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-rack:

      .. rst-class:: ansible-option-title

      **rack**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-rack" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the rack to assign the device to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-serial"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-serial:

      .. rst-class:: ansible-option-title

      **serial**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-serial" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Serial number of the device


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-site"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-site" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Required if \ :emphasis:`state=present`\  and the device does not exist yet


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-state:

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

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-status:

      .. rst-class:: ansible-option-title

      **status**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-status" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The status of the device

      Required if \ :emphasis:`state=present`\  and the device does not exist yet


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-tags"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-tags:

      .. rst-class:: ansible-option-title

      **tags**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-tags" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Any tags that the device may need to be associated with


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-tenant"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-tenant:

      .. rst-class:: ansible-option-title

      **tenant**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-tenant" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The tenant that the device will be assigned to


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-token:

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

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-url:

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

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-validate_certs:

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

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"true"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vc_position"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-vc_position:

      .. rst-class:: ansible-option-title

      **vc_position**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vc_position" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Position in the assigned virtual chassis


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vc_priority"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-vc_priority:

      .. rst-class:: ansible-option-title

      **vc_priority**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vc_priority" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Priority in the assigned virtual chassis


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-virtual_chassis"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__parameter-virtual_chassis:

      .. rst-class:: ansible-option-title

      **virtual_chassis**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-virtual_chassis" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`any`

      :ansible-option-versionadded:`added in 3.0.0 of networktocode.nautobot`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Virtual chassis the device will be assigned to


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
        - name: Create device within Nautobot with only required information
          networktocode.nautobot.device:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Test Device
            device_type: C9410R
            device_role: Core Switch
            site: Main
            status: active
            state: present

        - name: Create device within Nautobot with empty string name to generate UUID
          networktocode.nautobot.device:
            url: http://nautobot.local
            token: thisIsMyToken
            name: ""
            device_type: C9410R
            device_role: Core Switch
            site: Main
            status: active
            state: present

        - name: Delete device within nautobot
          networktocode.nautobot.device:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Test Device
            state: absent

        - name: Create device with tags
          networktocode.nautobot.device:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Another Test Device
            device_type: C9410R
            device_role: Core Switch
            site: Main
            status: active
            local_context_data:
              bgp: "65000"
            tags:
              - Schnozzberry
            state: present

        - name: Update the rack and position of an existing device
          networktocode.nautobot.device:
            url: http://nautobot.local
            token: thisIsMyToken
            name: Test Device
            rack: Test Rack
            position: 10
            face: Front
            state: present




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
        <div class="ansibleOptionAnchor" id="return-device"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__return-device:

      .. rst-class:: ansible-option-title

      **device**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-device" title="Permalink to this return value"></a>

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


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-msg"></div>

      .. _ansible_collections.networktocode.nautobot.device_module__return-msg:

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
- David Gomez (@amb1s1)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/nautobot/nautobot-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/nautobot/nautobot-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

