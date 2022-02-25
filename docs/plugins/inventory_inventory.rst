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

.. _ansible_collections.networktocode.nautobot.inventory_inventory:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.inventory inventory -- Nautobot inventory source
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This inventory plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 3.3.1).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.

    To use it in a playbook, specify: :code:`networktocode.nautobot.inventory`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Get inventory hosts from Nautobot


.. Aliases


.. Requirements


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
        <div class="ansibleOptionAnchor" id="parameter-ansible_host_dns_name"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-ansible_host_dns_name:

      .. rst-class:: ansible-option-title

      **ansible_host_dns_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ansible_host_dns_name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If True, sets DNS Name (fetched from primary_ip) to be used in ansible_host variable, instead of IP Address.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-api_endpoint"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-api_endpoint:

      .. rst-class:: ansible-option-title

      **api_endpoint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_endpoint" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Endpoint of the Nautobot API


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: NAUTOBOT\_URL


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-cache:

      .. rst-class:: ansible-option-title

      **cache**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Toggle to enable/disable the caching of the inventory's source data, requires a cache plugin setup to work.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [inventory]
          cache = no


      - Environment variable: ANSIBLE\_INVENTORY\_CACHE


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_connection"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-cache_connection:

      .. rst-class:: ansible-option-title

      **cache_connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_connection" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Cache connection data or path, read cache plugin documentation for specifics.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entries:

        .. code-block::

          [defaults]
          fact_caching_connection = None



        .. code-block::

          [inventory]
          cache_connection = None


      - Environment variable: ANSIBLE\_CACHE\_PLUGIN\_CONNECTION

      - Environment variable: ANSIBLE\_INVENTORY\_CACHE\_CONNECTION


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_plugin"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-cache_plugin:

      .. rst-class:: ansible-option-title

      **cache_plugin**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_plugin" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Cache plugin to use for the inventory's source data.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"memory"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entries:

        .. code-block::

          [defaults]
          fact_caching = memory



        .. code-block::

          [inventory]
          cache_plugin = memory


      - Environment variable: ANSIBLE\_CACHE\_PLUGIN

      - Environment variable: ANSIBLE\_INVENTORY\_CACHE\_PLUGIN


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_prefix"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-cache_prefix:

      .. rst-class:: ansible-option-title

      **cache_prefix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_prefix" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Prefix to use for cache plugin files/tables


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"ansible\_inventory\_"`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entries:

        .. code-block::

          [default]
          fact_caching_prefix = ansible_inventory_



        .. code-block::

          [inventory]
          cache_prefix = ansible_inventory_


      - Environment variable: ANSIBLE\_CACHE\_PLUGIN\_PREFIX

      - Environment variable: ANSIBLE\_INVENTORY\_CACHE\_PLUGIN\_PREFIX


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_timeout"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-cache_timeout:

      .. rst-class:: ansible-option-title

      **cache_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_timeout" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Cache duration in seconds


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`3600`

      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entries:

        .. code-block::

          [defaults]
          fact_caching_timeout = 3600



        .. code-block::

          [inventory]
          cache_timeout = 3600


      - Environment variable: ANSIBLE\_CACHE\_PLUGIN\_TIMEOUT

      - Environment variable: ANSIBLE\_INVENTORY\_CACHE\_TIMEOUT


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-compose"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-compose:

      .. rst-class:: ansible-option-title

      **compose**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-compose" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of custom ansible host vars to create from the device object fetched from Nautobot


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-config_context"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-config_context:

      .. rst-class:: ansible-option-title

      **config_context**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-config_context" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If True, it adds config_context in host vars.

      Config-context enables the association of arbitrary data to devices and virtual machines grouped by region, site, role, platform, and/or tenant. Please check official nautobot docs for more info.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-device_query_filters"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-device_query_filters:

      .. rst-class:: ansible-option-title

      **device_query_filters**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-device_query_filters" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of parameters passed to the query string for devices (Multiple values may be separated by commas)


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-dns_name"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-dns_name:

      .. rst-class:: ansible-option-title

      **dns_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-dns_name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Force IP Addresses to be fetched so that the dns_name for the primary_ip of each device or VM is set as a host_var.

      Setting interfaces will also fetch IP addresses and the dns_name host_var will be set.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-fetch_all"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-fetch_all:

      .. rst-class:: ansible-option-title

      **fetch_all**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-fetch_all" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      By default, fetching interfaces and services will get all of the contents of Nautobot regardless of query_filters applied to devices and VMs.

      When set to False, separate requests will be made fetching interfaces, services, and IP addresses for each device_id and virtual_machine_id.

      If you are using the various query_filters options to reduce the number of devices, querying Nautobot may be faster with fetch_all False.

      For efficiency, when False, these requests will be batched, for example /api/dcim/interfaces?limit=0&device_id=1&device_id=2&device_id=3

      These GET request URIs can become quite large for a large number of devices.

      If you run into HTTP 414 errors, you can adjust the max_uri_length option to suit your web server.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-default-bold:`yes` :ansible-option-default:`← (default)`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-flatten_config_context"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-flatten_config_context:

      .. rst-class:: ansible-option-title

      **flatten_config_context**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-flatten_config_context" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If \ :emphasis:`config\_context`\  is enabled, by default it's added as a host var named config_context.

      If flatten_config_context is set to True, the config context variables will be added directly to the host instead.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-flatten_custom_fields"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-flatten_custom_fields:

      .. rst-class:: ansible-option-title

      **flatten_custom_fields**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-flatten_custom_fields" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      By default, host custom fields are added as a dictionary host var named custom_fields.

      If flatten_custom_fields is set to True, the fields will be added directly to the host instead.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-flatten_local_context_data"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-flatten_local_context_data:

      .. rst-class:: ansible-option-title

      **flatten_local_context_data**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-flatten_local_context_data" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If \ :emphasis:`local\_context\_data`\  is enabled, by default it's added as a host var named local_context_data.

      If flatten_local_context_data is set to True, the config context variables will be added directly to the host instead.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-follow_redirects"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-follow_redirects:

      .. rst-class:: ansible-option-title

      **follow_redirects**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-follow_redirects" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Determine how redirects are followed.

      By default, \ :emphasis:`follow\_redirects`\  is set to uses urllib2 default behavior.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`urllib2` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`all`
      - :ansible-option-choices-entry:`yes`
      - :ansible-option-choices-entry:`safe`
      - :ansible-option-choices-entry:`none`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group_by"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-group_by:

      .. rst-class:: ansible-option-title

      **group_by**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group_by" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Keys used to create groups. The \ :emphasis:`plurals`\  option controls which of these are valid.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`sites`
      - :ansible-option-choices-entry:`site`
      - :ansible-option-choices-entry:`tenants`
      - :ansible-option-choices-entry:`tenant`
      - :ansible-option-choices-entry:`tenant\_group`
      - :ansible-option-choices-entry:`racks`
      - :ansible-option-choices-entry:`rack`
      - :ansible-option-choices-entry:`rack\_group`
      - :ansible-option-choices-entry:`rack\_role`
      - :ansible-option-choices-entry:`tags`
      - :ansible-option-choices-entry:`tag`
      - :ansible-option-choices-entry:`device\_roles`
      - :ansible-option-choices-entry:`role`
      - :ansible-option-choices-entry:`device\_types`
      - :ansible-option-choices-entry:`device\_type`
      - :ansible-option-choices-entry:`manufacturers`
      - :ansible-option-choices-entry:`manufacturer`
      - :ansible-option-choices-entry:`platforms`
      - :ansible-option-choices-entry:`platform`
      - :ansible-option-choices-entry:`region`
      - :ansible-option-choices-entry:`cluster`
      - :ansible-option-choices-entry:`cluster\_type`
      - :ansible-option-choices-entry:`cluster\_group`
      - :ansible-option-choices-entry:`is\_virtual`
      - :ansible-option-choices-entry:`services`
      - :ansible-option-choices-entry:`status`

      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group_names_raw"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-group_names_raw:

      .. rst-class:: ansible-option-title

      **group_names_raw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group_names_raw" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Will not add the group_by choice name to the group names


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-groups"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-groups:

      .. rst-class:: ansible-option-title

      **groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-groups" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Add hosts to group based on Jinja2 conditionals.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-interfaces"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-interfaces:

      .. rst-class:: ansible-option-title

      **interfaces**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-interfaces" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If True, it adds the device or virtual machine interface information in host vars.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-keyed_groups:

      .. rst-class:: ansible-option-title

      **keyed_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Add hosts to group based on the values of a variable.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-max_uri_length"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-max_uri_length:

      .. rst-class:: ansible-option-title

      **max_uri_length**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-max_uri_length" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      When fetch_all is False, GET requests to Nautobot may become quite long and return a HTTP 414 (URI Too Long).

      You can adjust this option to be smaller to avoid 414 errors, or larger for a reduced number of requests.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`4000`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plugin"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-plugin:

      .. rst-class:: ansible-option-title

      **plugin**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plugin" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      token that ensures this is a source file for the 'nautobot' plugin.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`networktocode.nautobot.inventory`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plurals"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-plurals:

      .. rst-class:: ansible-option-title

      **plurals**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plurals" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If True, all host vars are contained inside single-element arrays for legacy compatibility with old versions of this plugin.

      Group names will be plural (ie. "sites_mysite" instead of "site_mysite")

      The choices of \ :emphasis:`group\_by`\  will be changed by this option.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-default-bold:`yes` :ansible-option-default:`← (default)`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query_filters"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-query_filters:

      .. rst-class:: ansible-option-title

      **query_filters**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query_filters" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of parameters passed to the query string for both devices and VMs (Multiple values may be separated by commas)


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-services"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-services:

      .. rst-class:: ansible-option-title

      **services**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-services" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in 1.0.0 of networktocode.nautobot`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If True, it adds the device or virtual machine services information in host vars.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-default-bold:`yes` :ansible-option-default:`← (default)`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-strict"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-strict:

      .. rst-class:: ansible-option-title

      **strict**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-strict" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If \ :literal:`yes`\  make invalid entries a fatal error, otherwise skip and continue.

      Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-timeout"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Timeout for Nautobot requests in seconds


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`60`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-token:

      .. rst-class:: ansible-option-title

      **token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Nautobot API token to be able to read against Nautobot.

      This may not be required depending on the Nautobot setup.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: NAUTOBOT\_TOKEN


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Allows connection when SSL certificates are not valid. Set to \ :literal:`false`\  when certificates are not trusted.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`no`
      - :ansible-option-default-bold:`yes` :ansible-option-default:`← (default)`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-virtual_chassis_name"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-virtual_chassis_name:

      .. rst-class:: ansible-option-title

      **virtual_chassis_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-virtual_chassis_name" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      When a device is part of a virtual chassis, use the virtual chassis name as the Ansible inventory hostname.

      The host var values will be from the virtual chassis master.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vm_query_filters"></div>

      .. _ansible_collections.networktocode.nautobot.inventory_inventory__parameter-vm_query_filters:

      .. rst-class:: ansible-option-title

      **vm_query_filters**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vm_query_filters" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of parameters passed to the query string for VMs (Multiple values may be separated by commas)


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    # inventory.yml file in YAML format
    # Example command line: ansible-inventory -v --list -i inventory.yml

    plugin: networktocode.nautobot.inventory
    api_endpoint: http://localhost:8000
    validate_certs: True
    config_context: False
    group_by:
      - device_roles
    query_filters:
      - role: network-edge-router
    device_query_filters:
      - has_primary_ip: 'true'

    # has_primary_ip is a useful way to filter out patch panels and other passive devices

    # Query filters are passed directly as an argument to the fetching queries.
    # You can repeat tags in the query string.

    query_filters:
      - role: server
      - tag: web
      - tag: production

    # See the Nautobot documentation at https://nautobot.readthedocs.io/en/latest/api/overview/
    # the query_filters work as a logical **OR**
    #
    # Prefix any custom fields with cf_ and pass the field value with the regular Nautobot query string

    query_filters:
      - cf_foo: bar

    # Nautobot inventory plugin also supports Constructable semantics
    # You can fill your hosts vars using the compose option:

    plugin: networktocode.nautobot.inventory
    compose:
      foo: last_updated
      bar: display
      nested_variable: rack.display

    # You can use keyed_groups to group on properties of devices or VMs.
    # NOTE: It's only possible to key off direct items on the device/VM objects.
    plugin: networktocode.nautobot.inventory
    keyed_groups:
      - prefix: status
        key: status.value




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Remy Leone (@sieben)
- Anthony Ruhier (@Anthony25)
- Nikhil Singh Baliyan (@nikkytub)
- Sander Steffann (@steffann)
- Douglas Heriot (@DouglasHeriot)



.. Parsing errors

