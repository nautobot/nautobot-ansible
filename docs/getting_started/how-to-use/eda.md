# EDA Event Source Plugin

More information on Event-Driven Ansible is available at the [Ansible community documentation](https://ansible.readthedocs.io/projects/ansible-eda/).

Event source plugins describe the source of an event stream. For the Nautobot Change log source plugin, the plugin will query the log based on a configured interval. Five seconds by default.

The returned Change log objects are assigned to the event queue, and then processed by Ansible EDA.

## Use Case Ideas

- Trigger Ansible playbook/AWX/AAP(Tower) job templates based on event conditions
    - When a interface is changed in Nautobot trigger a playbook to execute that configuration change.
    - When a new device is created in Nautobot trigger a playbook to add that device to all your NMS tools.


## Running the Example

An example rulebook is provided in the collection.

```yml
---
# This example changes the polling interval to 5 seconds. It also adds query params to filter down the events coming into the platform.

- name: "Watch for new changelog entries"
  hosts: "localhost"
  sources:
    - networktocode.nautobot.nautobot_changelog:
        instance: "https://demo.nautobot.com"
        token: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        interval: 5
        validate_certs: true
        # query: "?time__gte={{ '2024-07-15 12:00:00' | to_datetime }}"
        query: ""

  rules:
    - name: "New changelog created"
      condition: "event.id is defined"
      # Action is triggered if condition is `true`.
      action:
        # For simple examples just print the event as a debug message.
        debug:

```

You can execute this example by running the rulebook via its FQDN.

```bash
ansible-rulebook --rulebook networktocode.nautobot.demo_nautobot_rulebook --print-events
```

The `--print-events` is a option to get all events printed to the terminal.

```
bash-5.1$ ansible-rulebook --rulebook networktocode.nautobot.demo_nautobot_rulebook --print-events

** 2025-03-15 14:36:03.207838 [collection] *********************************************************************************************************************************************************************************************
Loading rulebook from /app/.ansible/collections/ansible_collections/networktocode/nautobot/extensions/eda/rulebooks/demo_nautobot_rulebook.yml
****************************************************************************************************************************************************************************************************************************************

** 2025-03-15 14:36:04.449732 [received event] *****************************************************************************************************************************************************************************************
Ruleset: Watch for new changelog entries
Event:
{'approval_required': False,
 'approval_required_override': False,
 'created': '2025-03-15T04:01:37.503Z',
 'custom_fields': {},
 'default_job_queue': 'f575b43d-adb9-4315-8814-8d3a8c157819',
 'default_job_queue_override': False,
 'description': '',
 'description_override': False,
 'dryrun_default': False,
 'dryrun_default_override': False,
 'enabled': False,
 'grouping': 'Demo Designs',
 'grouping_override': False,
 'has_sensitive_variables': False,
 'has_sensitive_variables_override': False,
 'hidden': False,
 'hidden_override': False,
 'installed': True,
 'is_job_button_receiver': False,
 'is_job_hook_receiver': False,
 'is_singleton': False,
 'is_singleton_override': False,
 'job_class_name': 'CoreSiteDesign',
 'job_queues_override': False,
 'last_updated': '2025-03-15T04:01:38.576Z',
 'meta': {'received_at': '2025-03-15T14:36:04.448846Z',
          'source': {'name': 'networktocode.nautobot.nautobot_changelog',
                     'type': 'networktocode.nautobot.nautobot_changelog'},
          'uuid': '8d496cd9-5987-414a-9937-56bf6fe71703'},
 'module_name': 'demo_designs.jobs.core_site',
 'name': 'Backbone Site Design',
 'name_override': False,
 'read_only': False,
 'soft_time_limit': 0,
 'soft_time_limit_override': False,
 'supports_dryrun': True,
 'tags': [],
 'time_limit': 0,
 'time_limit_override': False}
****************************************************************************************************************************************************************************************************************************************

** 2025-03-15 14:36:04.451269 [received event] *****************************************************************************************************************************************************************************************
Ruleset: Watch for new changelog entries
Event:
{'branch': 'main',
 'created': '2025-03-15T04:01:36.631Z',
 'current_head': '398aee38734c552b869a33a41ce300903b539722',
 'custom_fields': {},
 'last_updated': '2025-03-15T04:01:37.349Z',
 'meta': {'received_at': '2025-03-15T14:36:04.449687Z',
          'source': {'name': 'networktocode.nautobot.nautobot_changelog',
                     'type': 'networktocode.nautobot.nautobot_changelog'},
          'uuid': '1eacd8fe-97e8-40cf-91b0-66c6bac74a52'},
 'name': 'Demo Designs',
 'provided_contents': ['extras.job'],
 'remote_url': 'https://github.com/nautobot/demo-designs.git',
 'secrets_group': None,
 'slug': 'demo_designs',
 'tags': []}
**********************************************************************************************************************************************************************************************************************************
```
