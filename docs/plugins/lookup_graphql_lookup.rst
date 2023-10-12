
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

.. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

networktocode.nautobot.lookup_graphql lookup -- Queries and returns elements from Nautobot GraphQL endpoint
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `networktocode.nautobot collection <https://galaxy.ansible.com/networktocode/nautobot>`_ (version 5.0.1).

    To install it, use: :code:`ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this lookup plugin,
    see :ref:`Requirements <ansible_collections.networktocode.nautobot.lookup_graphql_lookup_requirements>` for details.

    To use it in a playbook, specify: :code:`networktocode.nautobot.lookup_graphql`.

.. version_added

.. rst-class:: ansible-version-added

New in networktocode.nautobot 1.1.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Queries Nautobot via its GraphQL API through pynautobot


.. Aliases


.. Requirements

.. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this lookup.

- pynautobot






.. Options

Keyword parameters
------------------

This describes keyword parameters of the lookup. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``lookup('networktocode.nautobot.lookup_graphql', key1=value1, key2=value2, ...)`` and ``query('networktocode.nautobot.lookup_graphql', key1=value1, key2=value2, ...)``

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

      .. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup__parameter-api_version:

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

      The Nautobot Rest API Version to use


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-graph_variables"></div>

      .. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup__parameter-graph_variables:

      .. rst-class:: ansible-option-title

      **graph_variables**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-graph_variables" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Dictionary of keys/values to pass into the GraphQL query

      See [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query"></div>

      .. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup__parameter-query:

      .. rst-class:: ansible-option-title

      **query**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The GraphQL formatted query string, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html).


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup__parameter-token:

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

      The API token created through Nautobot


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`NAUTOBOT\_TOKEN`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-url"></div>

      .. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup__parameter-url:

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

      The URL to the Nautobot instance to query (http://nautobot.example.com:8000)


      .. rst-class:: ansible-option-line

      :ansible-option-configuration:`Configuration:`

      - Environment variable: :envvar:`NAUTOBOT\_URL`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>

      .. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup__parameter-validate_certs:

      .. rst-class:: ansible-option-title

      **validate_certs**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Whether or not to validate SSL of the Nautobot instance


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`true`

      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
      # Make API Query without variables
      - name: SET FACT OF STRING
        set_fact:
          query_string: |
            query {
              locations {
                id
                name
                parent {
                  name
                }
              }
            }

      # Make query to GraphQL Endpoint
      - name: Obtain list of locations from Nautobot
        set_fact:
          query_response: "{{ query('networktocode.nautobot.lookup_graphql', query=query_string, url='https://nautobot.example.com', token='<redact>') }}"

      # Example with variables
      - name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
        set_fact:
          graph_variables:
            location_name: DEN
          query_string: |
            query ($location_name:String!) {
                locations (name: $location_name) {
                id
                name
                parent {
                    name
                }
                }
            }

      # Get Response with variables
      - name: Obtain list of devices from Nautobot
        set_fact:
          query_response: "{{ query('networktocode.nautobot.lookup_graphql', query_string, graph_variables=graph_variables,
            url='https://nautobot.example.com', token='<redact>') }}"




.. Facts


.. Return values

Return Value
------------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-data"></div>

      .. _ansible_collections.networktocode.nautobot.lookup_graphql_lookup__return-data:

      .. rst-class:: ansible-option-title

      **data**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-data" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Data result from the GraphQL endpoint


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Josh VanDeraa (@jvanderaa)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/nautobot/nautobot-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/nautobot/nautobot-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

