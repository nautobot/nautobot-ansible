.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.networktocode.nautobot.gql_inventory_inventory:

.. Anchors: short name for ansible.builtin

.. Title

networktocode.nautobot.gql_inventory inventory -- Nautobot inventory source using GraphQL capability
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This inventory plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/ui/repo/published/networktocode/nautobot/>`_ (version 5.3.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this inventory plugin,
    see :ref:`Requirements <ansible_collections.networktocode.nautobot.gql_inventory_inventory_requirements>` for details.

    To use it in a playbook, specify: :code:`networktocode.nautobot.gql_inventory`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Get inventory hosts from Nautobot using GraphQL queries


.. Aliases


.. Requirements

.. _ansible_collections.networktocode.nautobot.gql_inventory_inventory_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this inventory.

- netutils






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
        <div class="ansibleOptionAnchor" id="parameter-api_endpoint"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-api_endpoint:

      .. rst-class:: ansible-option-title

      **api_endpoint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-api_endpoint" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Endpoint of the Nautobot API


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`NAUTOBOT\_URL`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-cache:

      .. rst-class:: ansible-option-title

      **cache**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Toggle to enable/disable the caching of the inventory's source data, requires a cache plugin setup to work.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [inventory]
          cache = false


      - Environment variable: :envvar:`ANSIBLE\_INVENTORY\_CACHE`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_connection"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-cache_connection:

      .. rst-class:: ansible-option-title

      **cache_connection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_connection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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
          fact_caching_connection = VALUE



        .. code-block::

          [inventory]
          cache_connection = VALUE


      - Environment variable: :envvar:`ANSIBLE\_CACHE\_PLUGIN\_CONNECTION`

      - Environment variable: :envvar:`ANSIBLE\_INVENTORY\_CACHE\_CONNECTION`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_plugin"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-cache_plugin:

      .. rst-class:: ansible-option-title

      **cache_plugin**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_plugin" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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


      - Environment variable: :envvar:`ANSIBLE\_CACHE\_PLUGIN`

      - Environment variable: :envvar:`ANSIBLE\_INVENTORY\_CACHE\_PLUGIN`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_prefix"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-cache_prefix:

      .. rst-class:: ansible-option-title

      **cache_prefix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_prefix" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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

          [defaults]
          fact_caching_prefix = ansible_inventory_



        .. code-block::

          [inventory]
          cache_prefix = ansible_inventory_


      - Environment variable: :envvar:`ANSIBLE\_CACHE\_PLUGIN\_PREFIX`

      - Environment variable: :envvar:`ANSIBLE\_INVENTORY\_CACHE\_PLUGIN\_PREFIX`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cache_timeout"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-cache_timeout:

      .. rst-class:: ansible-option-title

      **cache_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cache_timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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


      - Environment variable: :envvar:`ANSIBLE\_CACHE\_PLUGIN\_TIMEOUT`

      - Environment variable: :envvar:`ANSIBLE\_INVENTORY\_CACHE\_TIMEOUT`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-compose"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-compose:

      .. rst-class:: ansible-option-title

      **compose**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-compose" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Create vars from jinja2 expressions.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-default_ip_version"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-default_ip_version:

      .. rst-class:: ansible-option-title

      **default_ip_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-default_ip_version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Choice between IPv6 and IPv4 address as the primary IP for ansible\_host.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"IPv4"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"ipv4"`
      - :ansible-option-choices-entry:`"IPv6"`
      - :ansible-option-choices-entry:`"ipv6"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-follow_redirects"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-follow_redirects:

      .. rst-class:: ansible-option-title

      **follow_redirects**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-follow_redirects" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Determine how redirects are followed.

      By default, :emphasis:`follow\_redirects` is set to uses urllib2 default behavior.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"urllib2"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"all"`
      - :ansible-option-choices-entry:`"yes"`
      - :ansible-option-choices-entry:`"safe"`
      - :ansible-option-choices-entry:`"none"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group_by"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-group_by:

      .. rst-class:: ansible-option-title

      **group_by**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group_by" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of dot-sparated paths to index graphql query results (e.g. \`platform.display\`)

      The final value returned by each path is used to derive group names and then group the devices into these groups.

      Valid group names must be string, so indexing the dotted path should return a string (i.e. \`platform.display\` instead of \`platform\`)

      If value returned by the defined path is a dictionary, an attempt will first be made to access the \`name\` field, and then the \`display\` field. (i.e. \`platform\` would attempt to lookup \`platform.name\`, and if that data was not returned, it would then try \`platform.display\`)


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group_names_raw"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-group_names_raw:

      .. rst-class:: ansible-option-title

      **group_names_raw**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group_names_raw" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in networktocode.nautobot 4.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Will not add the group\_by choice name to the group names


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-groups"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-groups:

      .. rst-class:: ansible-option-title

      **groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-keyed_groups:

      .. rst-class:: ansible-option-title

      **keyed_groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`




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

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/default_value"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-keyed_groups/default_value:

      .. rst-class:: ansible-option-title

      **default_value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/default_value" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in ansible-core 2.12`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The default value when the host variable's value is an empty string.

      This option is mutually exclusive with :ansopt:`networktocode.nautobot.gql\_inventory#inventory:keyed\_groups[].trailing\_separator`.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/key"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-keyed_groups/key:

      .. rst-class:: ansible-option-title

      **key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/key" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The key from input dictionary used to generate groups


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/parent_group"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-keyed_groups/parent_group:

      .. rst-class:: ansible-option-title

      **parent_group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/parent_group" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      parent group for keyed group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/prefix"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-keyed_groups/prefix:

      .. rst-class:: ansible-option-title

      **prefix**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/prefix" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A keyed group name will start with this prefix


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/separator"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-keyed_groups/separator:

      .. rst-class:: ansible-option-title

      **separator**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/separator" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      separator used to build the keyed group name


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"\_"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-keyed_groups/trailing_separator"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-keyed_groups/trailing_separator:

      .. rst-class:: ansible-option-title

      **trailing_separator**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-keyed_groups/trailing_separator" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in ansible-core 2.12`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Set this option to :ansval:`False` to omit the :ansopt:`networktocode.nautobot.gql\_inventory#inventory:keyed\_groups[].separator` after the host variable when the value is an empty string.

      This option is mutually exclusive with :ansopt:`networktocode.nautobot.gql\_inventory#inventory:keyed\_groups[].default\_value`.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-leading_separator"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-leading_separator:

      .. rst-class:: ansible-option-title

      **leading_separator**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-leading_separator" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in ansible-core 2.11`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Use in conjunction with keyed\_groups.

      By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

      This is because the default prefix is "" and the default separator is "\_".

      Set this option to False to omit the leading underscore (or other separator) if no prefix is given.

      If the group name is derived from a mapping the separator is still used to concatenate the items.

      To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-plugin"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-plugin:

      .. rst-class:: ansible-option-title

      **plugin**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-plugin" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Setting that ensures this is a source file for the 'networktocode.nautobot' plugin.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"networktocode.nautobot.gql\_inventory"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-query:

      .. rst-class:: ansible-option-title

      **query**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      GraphQL query parameters or filters to send to Nautobot to obtain desired data


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`{}`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query/devices"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-query/devices:

      .. rst-class:: ansible-option-title

      **devices**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query/devices" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Additional query parameters or filters for devices


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query/virtual_machines"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-query/virtual_machines:

      .. rst-class:: ansible-option-title

      **virtual_machines**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query/virtual_machines" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`




      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Additional query parameters or filters for VMs


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-strict"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-strict:

      .. rst-class:: ansible-option-title

      **strict**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-strict" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If :ansval:`yes` make invalid entries a fatal error, otherwise skip and continue.

      Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-timeout"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-timeout:

      .. rst-class:: ansible-option-title

      **timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

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

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-token:

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

      Nautobot API token to be able to read against Nautobot.

      This may not be required depending on the Nautobot setup.


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`NAUTOBOT\_TOKEN`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-use_extra_vars"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-use_extra_vars:

      .. rst-class:: ansible-option-title

      **use_extra_vars**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-use_extra_vars" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in ansible-core 2.11`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Merge extra vars into the available variables for composition (highest precedence).


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - INI entry:

        .. code-block::

          [inventory_plugins]
          use_extra_vars = false


      - Environment variable: :envvar:`ANSIBLE\_INVENTORY\_USE\_EXTRA\_VARS`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Allows connection when SSL certificates are not valid. Set to :literal:`false` when certificates are not trusted.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


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
    # Add -vvv to the command to also see the GraphQL query that gets sent in the debug output.
    # Add -vvvv to the command to also see the JSON response that comes back in the debug output.

    # Minimum required parameters
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000  # Can be omitted if the NAUTOBOT_URL environment variable is set
    token: 1234567890123456478901234567  # Can be omitted if the NAUTOBOT_TOKEN environment variable is set

    # This will send the default GraphQL query of:
    # query {
    #   devices {
    #     name
    #     primary_ip4 {
    #       host
    #     }
    #     platform {
    #       napalm_driver
    #     }
    #   }
    #   virtual_machines {
    #     name
    #     primary_ip4 {
    #       host
    #     }
    #     platform {
    #       name
    #     }
    #   }
    # }

    # This module will automatically add the ansible_host key and set it equal to primary_ip4.host
    # as well as the ansible_network_os key and set it to platform.napalm_driver via netutils mapping
    # if the primary_ip4.host and platform.napalm_driver are present on the device in Nautobot.

    # Add additional query parameters with the query key.
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    query:
      devices:
        tags: name
        serial:
        tenant: name
        location:
          name:
          contact_name:
          description:
          parent: name
      virtual_machines:
        tags: name
        tenant: name

    # Add the default IP version to be used for the ansible_host
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    default_ip_version: ipv6
    query:
      devices:
        tags: name
        serial:
        tenant: name
        location:
          name:
          contact_name:
          description:
          parent: name
      virtual_machines:
        tags: name
        tenant: name

    # To group by use group_by key
    # Specify the full path to the data you would like to use to group by.
    # Ensure all paths are also included in the query.
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    query:
      devices:
        tags: name
        serial:
        tenant: name
        status: display
        location:
          name:
          contact_name:
          description:
          parent: name
      virtual_machines:
        tags: name
        tenant: name
        status: display
    group_by:
      - tenant.name
      - status.display

    # Filter output using any supported parameters.
    # To get supported parameters check the api/docs page for devices.
    # Add `filters` to any level of the dictionary and a filter will be added to the GraphQL query at that level.
    # (use -vvv to see the underlying GraphQL query being sent)
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    query:
      devices:
        filters:
          name__ic: ams
        interfaces:
          filters:
            name__ic: ethernet
          name:
          ip_addresses: address

    # You can filter to just devices/virtual_machines by filtering the opposite type to a name that doesn't exist.
    # For example, to only get devices:
    plugin: networktocode.nautobot.gql_inventory
    api_endpoint: http://localhost:8000
    query:
      virtual_machines:
        filters:
          name: EXCLUDE ALL



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this inventory:

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
        <div class="ansibleOptionAnchor" id="return-_list"></div>

      .. _ansible_collections.networktocode.nautobot.gql_inventory_inventory__return-_list:

      .. rst-class:: ansible-option-title

      **_list**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-_list" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      list of composed dictionaries with key and value


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Network to Code (@networktocode)
- Armen Martirosyan (@armartirosyan)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

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
