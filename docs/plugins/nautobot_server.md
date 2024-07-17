# networktocode.nautobot.nautobot_server

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.nautobot_server`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- No synopsis available.

## Requirements

- nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| args | dict |  | A dictionary of the optional arguments and their values used together with the command. This translates {"name_arg": "value_arg"} to "--name_arg value_arg". |
| command | str |  | The name of the Nautobot management command to run. Some command fully implemented are: `createsuperuser`, `migrate`, `makemigrations`, `post_upgrade` and `collectstatic`. Other commands can be entered, but will fail if they're unknown to Nautobot or use positional arguments. The module will perform some basic parameter validation, when applicable, to the commands. |
| db_password | str |  | Database password used in Nautobot. |
| db_username | str |  | Database username used in Nautobot. |
| flags | list |  | A list of flags to append to the command that is passed to `nautobot-server`, so that ["flag1", "flag2"] is translated to "--flag1 --flag2". |
| positional_args | list |  | A list of additional arguments to append to the end of the command that is passed to `nautobot-server`. These are appended to the end of the command, so that ["arg1", "arg2"] is translated to "arg1 arg2". |
| project_path | path |  | The path to the root of the Nautobot application where B(nautobot-server) lives. |
| pythonpath | path |  | A directory to add to the Python path. Typically used to include the settings module if it is located external to the application directory. |
| settings | path |  | The Python path to the application's settings module, such as 'myapp.settings'. |
| virtualenv | path |  | An optional path to a I(virtualenv) installation to use while running the nautobot-server application. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

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

| Key | Data Type | Description |
| --- | --------- | ----------- |
| changed | string | Boolean that is true if the command changed the state.<br>Returned: always |
| out | string | Raw output from the command execution.<br>Returned: always |
| cmd | string | Full command executed in the Server.<br>Returned: always |
| project_path | string | The path to the root of the Nautobot application where B(nautobot-server) lives.<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
