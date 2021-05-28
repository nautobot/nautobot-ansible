Nautobot Ansible Install Nautobot Notes
=======================================

Supported and Tested OSs
------------------------

The following OS’s are tested/supported. The support is expected to line
up with the supported OSs of Nautobot specifically. Issues related to
supported OSs will be taken. If the issue is on a tested but unsupported
OS, then the mileage may vary; issues are welcome but may have limited
response.

====== ======= ========= ======
OS     Version Supported Tested
====== ======= ========= ======
RHEL   7       No        Yes
RHEL   8       Yes       Yes
Ubuntu 18      No        Yes
Ubuntu 20      Yes       Yes
====== ======= ========= ======

Required Variables
------------------

The variables required need to be defined in the inventory or the
playbook for the host.

==================== ======= ==================================
Variable Name        Default Description
==================== ======= ==================================
cert_country                 Country for the certificate
cert_state                   State for the certificate
cert_city                    City for the certificate
cert_domain                  Domain for the certificate
nautobot_db_username         Username for the Nautobot database
nautobot_db_password         Password for the Nautobot database
nautobot_db_name             Name of the Nautobot database
redis_password               Password for the redis database
==================== ======= ==================================

Optional Variables
------------------

These variables control the operations of the playbook.

+------------------------------------------+----------+----------------+
| Variable Name                            | Default  | Description    |
+==========================================+==========+================+
| create_new_self_signed_cert              | False    | Boolean on     |
|                                          |          | whether or not |
|                                          |          | should create  |
|                                          |          | a new self     |
|                                          |          | signed cert    |
|                                          |          | when one       |
|                                          |          | exists         |
|                                          |          | already.       |
+------------------------------------------+----------+----------------+
| nautobot_http_port                       | “80”     | HTTP port to   |
|                                          |          | listen on      |
+------------------------------------------+----------+----------------+
| nautobot_https_port                      | “443”    | HTTPS port to  |
|                                          |          | listen on      |
+------------------------------------------+----------+----------------+

Gathered Variables in Playbook
------------------------------

These are the variables that are defined in the playbook execution.
These should be set if running your own playbook with the roles that are
provided.

+------------------------------+--------------+-----------------------+
| Variable Name                | Default      | Description           |
+==============================+==============+=======================+
| os_family                    | ansible      | lower                 |
|                              | _facts[      |                       |
|                              | ‘os_family’] |                       |
+------------------------------+--------------+-----------------------+
| os_version                   | ansible      | The major OS version, |
|                              | _facts[‘dist | 7/8 for RHEL flavors, |
|                              | ribution_maj | 18/20 for Debian      |
|                              | or_version’] | flavor                |
+------------------------------+--------------+-----------------------+
