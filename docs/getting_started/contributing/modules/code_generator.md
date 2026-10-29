# Module Code Generator

The modules in `plugins/modules/` are generated from the Nautobot REST API. Don't edit a generated module directly: change its config file in `development/codegen/modules/` and run the generator. Each generated module says so in its header comment.

Five modules are still written by hand, because they don't manage a REST API endpoint: `graphql_facts`, `graphql_info`, `nautobot_server`, `plugin` and `query_graphql`. They're listed under `hand_written_modules` in `development/codegen/config.yml`.

## Run the generator

The generator reads the API from the `nautobot` container of the development environment, so start it first:

```bash
invoke start
invoke codegen
```

`invoke codegen` does three things:

1. Runs `nautobot-server spectacular` in the container to get the OpenAPI schema for the API version set by `nautobot_ver` (3.2 by default).
2. Runs `development/codegen/dump_model_metadata.py` in the container with `nautobot-server shell`. The OpenAPI schema doesn't say which model a foreign key points to, which fields make up a model's natural key, or what the choices' display labels are; this script reads them from Nautobot's models and REST API serializers.
3. Runs `development/codegen/generate.py`, which updates the module configs and rewrites the modules and `plugins/module_utils/generated.py`.

Both downloads are saved in `development/codegen/.cache/` (ignored by git). Add `--skip-fetch` to reuse them, for example after editing a module config.

The generator prints a report of what changed in the API and what it did about it, and saves it as `development/codegen/.cache/report.txt`. Commit the changed module configs and modules together.

## What the generator does with API changes

For each module, the generator compares the module config with its API endpoint:

| API change | What the generator does |
| --- | --- |
| New endpoint | Writes a new module and module config, unless the endpoint is listed under `skip_endpoints` in `config.yml`. |
| New field on an existing endpoint | Adds an option with `version_added` set to the next minor release, unless the module is deprecated or the field is listed under `ignore_api_fields`. |
| New choice value | Adds it to the option's `choices`. |
| Field removed | Reports an error. Remove the option, or set `api_field: null` if the option isn't sent to the API as-is. |
| Field type, foreign key target or help text changed | Rewrites options the generator added (`managed: true`). Options written by hand are left alone. |

`version_added` for new modules and options is the minor release after the version in `galaxy.yml`. Set `next_version` in `config.yml` to override it.

### Errors that need a person

The generator stops with an error (exit code 1) when it can't decide safely. The common cases are:

- **An option would be looked up on the wrong endpoint.** `CONVERT_TO_ID` in `plugins/module_utils/utils.py` maps option names to endpoints for every module at once. If a module has an option with the same name as a `CONVERT_TO_ID` key but the API field points to a different object type, values would be looked up on the wrong endpoint. The generator renames new options to avoid this (for example `group` becomes `dynamic_group` on `dynamic_group_membership`). When it can't, add the option to the module config yourself with a different name and `api_field` set to the API field, or add the field to `ignore_api_fields`.
- **A hand-written option already has the problem.** Fix the option, or add `known_issue: <reason>` to it in the module config. That turns the error into a warning and records why.

## Module configs

Each file in `development/codegen/modules/` contains everything needed to write one module. The generator rewrites these files, so comments in them are lost. The main keys are:

- `api_path`: the REST API list endpoint, such as `/dcim/cables/`.
- `options`: one entry per module option.
    - `api_field`: the API field the option is sent as, or `null` for options that aren't API fields (such as inline `vrfs` on devices).
    - `managed`: `true` when the generator created the option and manages it. It rewrites the argument spec and documentation from the API on every run, but keeps `description` and `version_added` once they're set, so you can improve a generated description.
    - `argument_spec` and `documentation`: what goes into the module's `argument_spec` and `DOCUMENTATION`.
    - `known_issue`: see above.
- `ignore_api_fields`: API fields this module never gets options for, with the reason.
- `lookup_fields`: the fields used to find an existing object, added to `ALLOWED_QUERY_PARAMS`. The generator uses the model's natural key when each part of it is an API field that the list endpoint can filter on, and otherwise `name`. When neither works the list is empty, the module finds objects by `id` only, and the report includes a warning. Modules that existed before the generator have `lookup_fields: null` and use the hand-written entries in `utils.py`.
- `generated_examples`: `true` when the generator writes `EXAMPLES`. Set it to `false` to keep examples you wrote.
- `shared_specs`, `ansible_module_kwargs`, `instance_kwargs`, `post_module_code`, `extra_imports`: the parts of `main()` that differ between modules. `instance_kwargs` contains the keyword arguments passed to the `Nautobot*Module` class, such as `remove_keys`.

## Lookup tables

The generator writes `plugins/module_utils/generated.py` with entries for `API_APPS_ENDPOINTS`, `ENDPOINT_NAME_MAPPING`, `CONVERT_TO_ID`, `QUERY_TYPES` and `ALLOWED_QUERY_PARAMS`. `utils.py` merges them into its own tables when it's imported, and when both define the same key, the hand-written entry in `utils.py` is used.

The generator only adds a `CONVERT_TO_ID` entry for a generated option when every module that uses the option name points it at the same object type. Otherwise the option accepts an ID or a dictionary of attributes, and the report has a warning.

`GENERATED_ENDPOINT_CONVERT_KEYS` maps renamed options back to their API field names, per endpoint; `NautobotModule._convert_identical_keys()` applies it.

`GENERATED_ENDPOINT_WRITE_ONLY_FIELDS` lists, per endpoint, the generated options whose API field is write-only, such as `namespace` on IP address ranges. The API doesn't return these fields, so `NautobotModule._update_object()` leaves them out when it checks whether the object changed. They're still sent when another field changes, but a change to a write-only field alone isn't detected.

## Continuous integration

CI should run the generator tests and `invoke codegen --check` against Nautobot 3.2. The check exits with code 1 when the committed modules don't match what the generator writes, or when the report has errors, and prints the difference. Add this job to `.github/workflows/tests.yml`:

```yaml
  codegen:
    runs-on: "${{ inputs.runs-on }}"
    env:
      INVOKE_NAUTOBOT_ANSIBLE_NAUTOBOT_VER: "3.2"
    steps:
      - name: "Check out repository code"
        uses: "actions/checkout@v6"
      - name: "Setup environment"
        uses: "networktocode/gh-action-setup-poetry-environment@v7"
      - name: "Code generator tests"
        run: "poetry run invoke codegen-tests"
      - name: "Start Nautobot"
        run: "poetry run invoke start"
      - name: "Check the generated modules"
        run: "poetry run invoke codegen --check"
      - name: "Upload the API drift report"
        if: "always()"
        uses: "actions/upload-artifact@v7"
        with:
          name: "codegen-report"
          path: "development/codegen/.cache/report.txt"
          if-no-files-found: "ignore"
```

When Nautobot releases a new version, raise `nautobot_ver` and run `invoke codegen`: the report lists every API change that affects the modules.

## Other tools

- `invoke codegen-tests` runs the generator's tests in `development/codegen/tests/`.
- `poetry run python -m development.codegen.compare --ref origin/develop` lists, for each module, the options added, removed or changed compared with a git ref. It ignores formatting, so it's a quick way to review a regenerated module.
- `development/codegen/bootstrap.py` turned the hand-written modules into module configs when the generator was introduced. You don't need to run it again.
