# Debugging

Unlike when developing Nautobot apps or developing for the core Nautobot project, there is no long-running process to attach a debugger to when working on Ansible modules. The [Ansible Community Documentation](https://docs.ansible.com/ansible/latest/dev_guide/debugging.html) offers some options for debugging.

As described there, if you don't need any complex interactions, faster debugging iteration can be achieved by [verifying your module code locally](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#verifying-your-module-code-locally). In fact, this workflow can be so useful that it has been streamlined in this collection's repo. We'll describe that next.

## Verifying your module code independently of Ansible

The following folders exist to help you debug your module code independently of other Ansible code:

- `./debugging_args/` - Folder for JSON debugging args files when testing modules independently
- `./debugging_args/*.json.example` - Example JSON debugging args file(s) for use when testing modules independently

To test a module independently:

1. **Create a JSON debugging args file** - create a file like `./debugging_args/your_module_name.json`. You can use the example file(s) to understand the target structure; this file should contain the JSON arguments you want to test, wrapped inside `ANSIBLE_MODULE_ARGS`.

    !!! tip
        As demonstrated in the example file(s), you can use `_ansible_check_mode` to signal to your module that it should run in `--check` mode.

    !!! note
        Naming your JSON debugging args file with `your_module_name` matching the real name of the module in `./plugins/modules/` is a good idea to make the Microsoft Visual Studio Code integrated debugging [described below](#vs-code-integrated-debugging) work seamlessly.

    !!! note
        All files in `./debugging_args/` except `*.example` are ignored by `git`, so it's safe enough to put data here for testing as long as you follow the note above.

2. **Force (re-)install the collection** - you can (re-)install into `./collections/` using `invoke galaxy-install --force`.

    !!! warning
        You need to make sure you do this every time you make a change in `./plugins/` to ensure you're testing the latest code.

3. **Run your module** - from the root folder of the repository, you can now run your module like so, passing in the arguments file:
```
export PYTHONPATH=./collections && python -m ansible_collections.networktocode.nautobot.plugins.modules.location_type ./debugging_args/location_type.json | jq .
```
Here are the first few lines of the output:
```
{
  "changed": true,
  "msg": "location_type My Location Type created",
  "diff": {
    "before": {
      "state": "absent"
    },
    "after": {
      "state": "present"
    }
  },
  "location_type": {
    "id": "2e3da039-a1e2-4faa-9b20-87486db6555d",
    "object_type": "dcim.locationtype",
    "display": "My Location Type",
...
```
Similarly, `pdb` works fine and can be used as usual just by adding in `-m pdb`:
```
> /{REMOVED}/collections/ansible_collections/networktocode/nautobot/plugins/modules/location_type.py(6)<module>()
-> from __future__ import absolute_import, division, print_function
(Pdb) c

{"changed": false, "msg": "location_type My Location Type already exists", "location_type": {"id": "5416fd14-0c14-49e7-8620-2ec4940414ac", "object_type": "dcim.locationtype", "display": "My Location Type", "url": "http://localhost:8000/api/dcim/location-types/5416fd14-0c14-49e7-8620-2ec4940414ac/", "natural_slug": "my-location-type_5416", "tree_depth": null, "content_types": ["dcim.device"], "name": "My Location Type", "description": "My Location Type Description", "nestable": false, "parent": null, "created": "2025-02-28T10:41:47.679777Z", "last_updated": "2025-02-28T10:41:47.679792Z", "notes_url": "http://localhost:8000/api/dcim/location-types/5416fd14-0c14-49e7-8620-2ec4940414ac/notes/", "custom_fields": {}}, "invocation": {"module_args": {"url": "http://localhost:8000", "token": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER", "name": "My Location Type", "description": "My Location Type Description", "nestable": false, "content_types": ["dcim.device"], "state": "present", "validate_certs": true, "query_params": null, "api_version": null, "custom_fields": null, "parent_location_type": null}}}
The program exited via sys.exit(). Exit status: 0
> /{REMOVED}/collections/ansible_collections/networktocode/nautobot/plugins/modules/location_type.py(6)<module>()
-> from __future__ import absolute_import, division, print_function
(Pdb) q
```
## Microsoft Visual Studio Code integration

### VS Code Workspace configuration file

For users of VS Code, the following file(s) are included to ease development. The specific uses are covered in more detail in later sections:

- `./nautobot-ansible.code-workspace - VS Code workspace configuration file

### VS Code tasks

As described in [Testing Locally](testing_locally.md), various Invoke commands are used to trigger build and test tasks. These remain the primary way of performing these actions, but the included workspace configuration file offers a non-exhaustive set of [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks) task automations for convenience that trigger the Invoke tasks.

You can trigger VS Code tasks using **Terminal > Run Task** or by pressing **Ctrl+Shift+B** / **Cmd+Shift+B**. Since these trigger Invoke, their behaviour is the same. Here's the list, each along with its Invoke equivalent:

- Build Nautobot docker image. (`invoke build`)
- Start Nautobot and its dependencies in detached mode. (`invoke start`)
- Stop Nautobot and its dependencies. (`invoke stop`)
- Build and serve docs locally for development. (`invoke docs`)
- Build the collection. (`invoke galaxy-build`)
- Install the collection. (`invoke galaxy-install`)
- Force (re-)build the collection. (`invoke galaxy-build --force`)
- Force (re-)install the collection. (`invoke galaxy-install --force`)

### VS Code integrated debugging

`pdb` is a good solution, but the scaffolding described above also makes it really easy to debug using VS Code's integrated debugger.

Just open either a JSON debugging args file from `./debugging_args/` or a module file from `./collections/ansible_collections/networktocode/nautobot/plugins/modules/` in the editor and launch VS Code's integrated debugger as usual, either using the keyboard shortcut `F5` or through the GUI by clicking the green play button in the `Run and Debug` panel. Setting breakpoints and so on works as you would expect.

!!! tip
    Both of these work seamlessly, because the `launch` configuration in the `.code-workspace` file uses `${fileBasenameNoExtension}`, which is the same for both files.
