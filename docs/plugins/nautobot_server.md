# networktocode.nautobot.nautobot_server

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.nautobot_server`.

+++ 3.0.0
    Added in 3.0.0.

## Synopsis

- Manages Nautobot Server using the C(nautobot-server) application frontend to C(django-admin). With the C(virtualenv) parameter
- all management commands will be executed by the given C(virtualenv) installation.

## Requirements

The below requirements are needed on the host that executes this module.

- nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| args | dict |  | A dictionary of the optional arguments and their values used together with the command.
This translates {"name_arg": "value_arg"} to "--name_arg value_arg".
 |
| command | str |  | The name of the Nautobot management command to run. Some command fully implemented are: `createsuperuser`,
`migrate`, `makemigrations`, `post_upgrade` and `collectstatic`.
Other commands can be entered, but will fail if they're unknown to Nautobot or use positional arguments.
The module will perform some basic parameter validation, when applicable, to the commands.
 |
| db_password | str |  | Database password used in Nautobot. |
| db_username | str |  | Database username used in Nautobot. |
| flags | list |  | A list of flags to append to the command that is passed to `nautobot-server`, so that ["flag1", "flag2"] is translated to "--flag1 --flag2". |
| positional_args | list |  | A list of additional arguments to append to the end of the command that is passed to `nautobot-server`. These are appended to the end of the command, so that ["arg1", "arg2"] is translated to "arg1 arg2". |
| project_path | path |  | The path to the root of the Nautobot application where __nautobot-server__ lives. |
| pythonpath | path |  | A directory to add to the Python path. Typically used to include the settings module if it is located external to the application directory. |
| settings | path |  | The Python path to the application's settings module, such as 'myapp.settings'. |
| virtualenv | path |  | An optional path to a _virtualenv_ installation to use while running the nautobot-server application. |

## Tags

!!! note "Note"
    * Inspired from Django_manage (U(https://github.com/ansible-collections/community.general/blob/main/plugins/modules/web_infrastructure/django_manage.py)).
    * To be able to use the C(collectstatic) command, you must have enabled staticfiles in your nautbot_config.py.
    * Your C(nautobot-server) application must be executable (rwxr-xr-x), and must have a valid shebang.

## Examples

```yaml

  - name: Createsuperuser
    networktocode.nautobot.nautobot_server:
      command: "createsuperuser"
      args:
        email: "admin93@example.com"
        username: "superadmin7"
      db_password: "{{ db_password }}"
  - name: Collectstatic
    networktocode.nautobot.nautobot_server:
      command: "collectstatic"
      db_password: "{{ db_password }}"
  - name: Post Upgrade
    networktocode.nautobot.nautobot_server:
      command: "post_upgrade"
  - name: Make Migrations for Plugin
    networktocode.nautobot.nautobot_server:
      command: "makemigrations"
      positional_args: ["my_plugin_name"]
      db_password: "{{ db_password }}"
  - name: Migrate Plugin
    networktocode.nautobot.nautobot_server:
      command: "migrate"
      args:
        verbosity: 3
      flags: ["merge"]
      positional_args: ["my_plugin_name"]
      db_username: "{{ db_username }}"
      db_password: "{{ db_password }}"

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| changed | bool | Boolean that is true if the command changed the state. | always |
| cmd | str | Full command executed in the Server. | always |
| out | str | Raw output from the command execution. | always |
| project_path | str | The path to the root of the Nautobot application where B(nautobot-server) lives. | always |

## Authors

- Network to Code (@networktocode)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
