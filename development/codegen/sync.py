"""Compare module configs with the Nautobot REST API and update them.

The generator creates and manages some options (`managed: true`) and rewrites them from the API on every run. Options written by
hand are only checked: the generator reports API changes that affect them but never edits them.
"""

import datetime
import re
from dataclasses import dataclass, field

# Ansible-test flags option names that look like secrets unless they set no_log.
NO_LOG_NAME = re.compile(r"pass(?!ive)|secret|token|key|psk", re.IGNORECASE)
SECRET_VALUE_NAME = re.compile(r"password|secret|token|psk|pre_shared", re.IGNORECASE)

ERROR = "error"
WARNING = "warning"
INFO = "info"


@dataclass
class Message:
    """One line of the drift report."""

    level: str
    module: str
    text: str

    def __str__(self):
        return f"{self.level.upper():7} {self.module}: {self.text}"


@dataclass
class Report:
    """Changes and problems found while comparing the module configs with the API."""

    messages: list = field(default_factory=list)

    def add(self, level, module, text):
        """Record a message about a module (or an endpoint path, for endpoints without a module)."""
        self.messages.append(Message(level, module, text))

    @property
    def errors(self):
        """Messages that need someone to change a config before the generator can finish."""
        return [message for message in self.messages if message.level == ERROR]

    def __str__(self):
        order = {ERROR: 0, WARNING: 1, INFO: 2}
        messages = sorted(self.messages, key=lambda message: (order[message.level], message.module, message.text))
        return "\n".join(str(message) for message in messages)


def option_name_for_field(api_field, context, options):
    """Pick the option name for an API field, or None if every candidate clashes with the global lookup tables.

    utils.py looks up CONVERT_TO_ID and CONVERT_KEYS by option name for every module, so an option can't reuse a
    name that those tables already give a different meaning. In that case the option is named after the object
    type it points to (for example `dynamic_group` instead of `group`).
    """
    hand = context.hand_tables
    target = context.endpoint_for_model(api_field.related_model) if api_field.related_model else None

    def clashes(name):
        if name in hand["CONVERT_KEYS"]:
            return True
        if name in hand["CONVERT_TO_ID"]:
            if target is None or api_field.content_type:
                return True
            lookup_endpoint = hand["CONVERT_TO_ID"][name]
            return lookup_endpoint != target.endpoint or context.find_app(lookup_endpoint) != target.app
        return False

    if not clashes(api_field.name):
        return api_field.name
    if target is not None and not api_field.content_type:
        candidate = hand["ENDPOINT_NAME_MAPPING"].get(target.endpoint) or module_name_for_endpoint(target)
        if candidate not in options and not clashes(candidate):
            return candidate
    return None


def describe_field(api_field, endpoint):
    """Return the description lines for a generated option."""
    verbose_name = endpoint.verbose_name
    if api_field.help_text:
        text = " ".join(api_field.help_text.split())
        # Some help texts are built from two strings joined without a space ("properties.May be null").
        text = re.sub(r"\.(?=[A-Z])", ". ", text)
        lines = [text]
    else:
        label = api_field.name.replace("_", " ")
        lines = [f"The {label} of the {verbose_name}"]
    if api_field.required:
        lines.append(f"Required if I(state=present) and the {verbose_name} does not exist yet")
    return lines


def argument_spec_for_field(api_field):
    """Return the argument_spec entry for a generated option."""
    spec = {"required": False}
    if api_field.related_model and not api_field.content_type:
        if api_field.many:
            spec.update(type="list", elements="raw")
        else:
            spec["type"] = "raw"
    elif api_field.content_type:
        # Content types are written as "app_label.model" strings.
        if api_field.many:
            spec.update(type="list", elements="str")
        else:
            spec["type"] = "str"
    elif api_field.json_type == "boolean":
        spec["type"] = "bool"
    elif api_field.json_type == "integer":
        spec["type"] = "int"
    elif api_field.json_type == "number":
        spec["type"] = "float"
    elif api_field.json_type == "array":
        spec["type"] = "list"
        spec["elements"] = {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}.get(
            api_field.json_items_type, "raw"
        )
    elif api_field.json_type == "object":
        spec["type"] = "dict"
    elif api_field.json_type == "string":
        spec["type"] = "str"
    else:
        spec["type"] = "raw"

    if api_field.choices and spec["type"] in ("str", "list"):
        choices = [choice for choice in api_field.choices if choice != ""]
        if choices:
            spec["choices"] = choices

    if NO_LOG_NAME.search(api_field.name):
        is_secret = spec["type"] == "str" and SECRET_VALUE_NAME.search(api_field.name)
        spec["no_log"] = bool(is_secret)
    return spec


def documentation_for_spec(spec, description, version_added=None):
    """Return the DOCUMENTATION entry matching an argument_spec entry."""
    doc = {"description": description, "required": spec.get("required", False), "type": spec["type"]}
    if "elements" in spec:
        doc["elements"] = spec["elements"]
    if "choices" in spec:
        doc["choices"] = spec["choices"]
    if "default" in spec:
        doc["default"] = spec["default"]
    if version_added:
        doc["version_added"] = version_added
    return doc


def managed_option(api_field, endpoint, version_added=None, previous=None):
    """Create or rewrite a generator-managed option, keeping the description and version_added already set."""
    spec = argument_spec_for_field(api_field)
    previous_doc = (previous or {}).get("documentation", {})
    description = previous_doc.get("description") or describe_field(api_field, endpoint)
    version_added = previous_doc.get("version_added", version_added)
    option = {
        "api_field": api_field.name,
        "managed": True,
        "argument_spec": spec,
        "documentation": documentation_for_spec(spec, description, version_added),
    }
    if (previous or {}).get("known_issue"):
        option["known_issue"] = previous["known_issue"]
    return option


def module_name_for_endpoint(endpoint):
    """Return the module name for a new endpoint, based on the model's verbose name (`IP address range`)."""
    return re.sub(r"[^a-z0-9]+", "_", endpoint.verbose_name.lower()).strip("_")


def natural_key_fields(endpoint):
    """Return the API fields that identify an object on this endpoint, for ALLOWED_QUERY_PARAMS.

    Uses the model's natural key when every part of it is a writable API field that the list endpoint can
    filter on. Otherwise falls back to `name`, and otherwise returns an empty list: the module then finds objects
    by `id` only, because guessing could match and update the wrong object.
    """

    def usable(name):
        return name in endpoint.fields and name in endpoint.filter_params

    fields = []
    for lookup in endpoint.natural_key:
        name = lookup.split("__")[0]
        if not usable(name):
            fields = []
            break
        if name not in fields:
            fields.append(name)
    if fields:
        return fields
    if usable("name"):
        return ["name"]
    return []


def primary_lookup(endpoint):
    """Return the field used to find an object on this endpoint from a single string value (for QUERY_TYPES)."""
    for lookup in endpoint.natural_key:
        if "__" not in lookup and lookup in endpoint.fields and lookup in endpoint.filter_params:
            if not endpoint.fields[lookup].related_model:
                return lookup
    for candidate in ("name", "model", "username", "value"):
        if candidate in endpoint.fields and candidate in endpoint.filter_params:
            return candidate
    return None


def next_minor_version(version):
    """Return the next minor release after a version (`6.3.0` -> `6.4.0`)."""
    major, minor, *_ = (int(part) for part in version.split("."))
    return f"{major}.{minor + 1}.0"


def new_module_config(name, endpoint, app_utils, next_version, shared_specs_available):
    """Return the config for a module that doesn't exist yet."""
    utils_module, class_name = app_utils
    plural = endpoint.path.strip("/").split("/")[1].replace("-", " ")
    shared_specs = ["NAUTOBOT_ARG_SPEC", "ID_ARG_SPEC"]
    fragments = ["networktocode.nautobot.fragments.base", "networktocode.nautobot.fragments.id"]
    notes = []
    if endpoint.tags_supported:
        shared_specs.append("TAGS_ARG_SPEC")
        fragments.append("networktocode.nautobot.fragments.tags")
        notes.append("Tags should be defined as a YAML list")
    if endpoint.custom_fields_supported:
        shared_specs.append("CUSTOM_FIELDS_ARG_SPEC")
        fragments.append("networktocode.nautobot.fragments.custom_fields")
    if endpoint.supports_contacts:
        shared_specs.append("CONTACTS_AND_TEAMS_ARG_SPEC")
        fragments.append("networktocode.nautobot.fragments.contacts_and_teams")
    if endpoint.supports_notes:
        shared_specs.append("NOTES_ARG_SPEC")
        fragments.append("networktocode.nautobot.fragments.notes")
    shared_specs = [spec for spec in shared_specs if spec in shared_specs_available]
    notes.append("This should be ran with connection C(local) and hosts C(localhost)")

    instance_var = name if name not in ("module", "main", "deepcopy") else f"nb_{name}"
    return {
        "module": name,
        "api_path": endpoint.path,
        "endpoint": endpoint.endpoint,
        "header": [
            f"# Copyright: (c) {datetime.date.today().year}, Network to Code (@networktocode) <info@networktocode.com>",
            "# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)",
        ],
        "utils_module": utils_module,
        "class_name": class_name,
        "endpoint_constant": None,
        "instance_var": instance_var,
        "instance_kwargs": {},
        "main_docstring": "\n    Main entry point for module execution.\n    ",
        "shared_specs": shared_specs,
        "ansible_module_kwargs": {"supports_check_mode": True},
        "extra_imports": [],
        "post_module_code": [],
        "ignore_api_fields": {},
        "lookup_fields": natural_key_fields(endpoint),
        "generated_examples": True,
        "options": {},
        "documentation": {
            "module": name,
            "short_description": f"Create, update or delete {plural} within Nautobot",
            "description": [f"Creates, updates or removes {plural} from Nautobot."],
            "notes": notes,
            "author": ["Network to Code (@networktocode)"],
            "version_added": next_version,
            "extends_documentation_fragment": fragments,
        },
        "examples": "",
        "return": RETURN_TEMPLATE.format(name=name),
    }


RETURN_TEMPLATE = """
{name}:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""


def _example_value(api_field):
    spec = argument_spec_for_field(api_field)
    if api_field.name == "status":
        return "Active"
    if spec.get("choices"):
        return spec["choices"][0]
    if spec["type"] == "bool":
        return True
    if spec["type"] in ("int", "float"):
        return 1
    if spec["type"] == "dict":
        return {}
    if spec["type"] == "list":
        return []
    if api_field.content_type:
        return "dcim.device"
    label = api_field.name.replace("_", " ").title()
    return f"Test {label}"


def generate_examples(config, endpoint):
    """Write EXAMPLES for a new module: create with the required fields, then delete by the same lookup fields."""
    from .render import to_yaml  # pylint: disable=import-outside-toplevel

    name = config["module"]
    verbose_name = endpoint.verbose_name
    required = {}
    for field_name, api_field in endpoint.fields.items():
        option_name = _option_for_api_field(config, field_name)
        if api_field.required and option_name:
            required[option_name] = _example_value(api_field)
    lookup = {}
    for field_name in config.get("lookup_fields") or []:
        option_name = _option_for_api_field(config, field_name)
        if option_name and field_name in endpoint.fields:
            lookup[option_name] = required.get(option_name, _example_value(endpoint.fields[field_name]))
    connection = {"url": "http://nautobot.local", "token": "thisIsMyToken"}
    tasks = [
        {
            "name": f"Create {verbose_name} within Nautobot with only required information",
            f"networktocode.nautobot.{name}": {**connection, **required, "state": "present"},
        },
        {
            "name": f"Delete {verbose_name} within Nautobot",
            f"networktocode.nautobot.{name}": {**connection, **(lookup or required), "state": "absent"},
        },
        {
            "name": f"Delete {verbose_name} by id",
            f"networktocode.nautobot.{name}": {
                **connection,
                "id": "00000000-0000-0000-0000-000000000000",
                "state": "absent",
            },
        },
    ]
    playbook = [
        {
            "name": "Test Nautobot modules",
            "connection": "local",
            "hosts": "localhost",
            "gather_facts": False,
            "tasks": tasks,
        }
    ]
    return "\n" + to_yaml(playbook)


def _option_for_api_field(config, field_name):
    for option_name, option in config["options"].items():
        if option.get("api_field") == field_name:
            return option_name
    return None


@dataclass
class Context:
    """Values shared by every module during one generator run."""

    endpoints: dict
    next_version: str
    global_ignored_fields: set
    shared_spec_options: dict
    hand_tables: dict
    report: Report = field(default_factory=Report)

    def find_app(self, endpoint_name, generated_apps=None):
        """Return the app utils.py's `_find_app()` would pick for an endpoint name: the first app that lists it."""
        for app, endpoints in self.hand_tables["API_APPS_ENDPOINTS"].items():
            if endpoint_name in endpoints:
                return app
        for app, endpoints in (generated_apps or {}).items():
            if endpoint_name in endpoints:
                return app
        return None

    def endpoint_for_model(self, model_label):
        """Return the Endpoint for a model label such as `dcim.cabletype`, or None."""
        for endpoint in self.endpoints.values():
            if endpoint.model == model_label:
                return endpoint
        return None


def sync_module(config, endpoint, context, is_new=False):
    """Update a module config to match its API endpoint and record what changed in the report."""
    name = config["module"]
    options = config["options"]
    deprecated = "deprecated" in config["documentation"]
    ignored = set(config.get("ignore_api_fields") or {}) | context.global_ignored_fields
    shared_options = set()
    for spec_name in config["shared_specs"]:
        shared_options.update(context.shared_spec_options.get(spec_name, {}))

    # Options whose API field no longer exists.
    for option_name, option in options.items():
        api_field = option.get("api_field")
        if api_field and api_field not in endpoint.fields:
            context.report.add(
                ERROR,
                name,
                f"option '{option_name}' maps to API field '{api_field}', which {endpoint.path} no longer accepts. "
                "Remove the option or set `api_field: null` in its config.",
            )

    # Generator-managed options are rewritten from the API on every run.
    for option_name, option in list(options.items()):
        api_field = option.get("api_field")
        if option.get("managed") and api_field in endpoint.fields:
            rebuilt = managed_option(endpoint.fields[api_field], endpoint, previous=option)
            if rebuilt != option:
                context.report.add(INFO, name, f"updated option '{option_name}' from the API")
            options[option_name] = rebuilt

    # Hand-written options: add choice values the API accepts that the option rejects.
    for option_name, option in options.items():
        api_field = endpoint.fields.get(option.get("api_field") or "")
        choices = (option.get("argument_spec") or {}).get("choices")
        if option.get("managed") or not api_field or not api_field.choices or not choices:
            continue
        # Hand-written options often accept the display labels too (CONVERT_CHOICES converts them).
        accepted = {str(choice).lower() for choice in choices}
        labels = api_field.choice_labels or [None] * len(api_field.choices)
        missing = [
            value
            for value, label in zip(api_field.choices, labels)
            if value and value.lower() not in accepted and (label is None or label.lower() not in accepted)
        ]
        if not missing:
            continue
        if deprecated:
            context.report.add(
                INFO,
                name,
                f"option '{option_name}' doesn't accept the API choices {', '.join(missing)}, "
                "not added because the module is deprecated",
            )
            continue
        choices.extend(missing)
        doc_choices = (option.get("documentation") or {}).get("choices")
        if doc_choices is not None and doc_choices is not choices:
            doc_choices.extend(choice for choice in missing if choice not in doc_choices)
        context.report.add(INFO, name, f"added API choices to option '{option_name}': {', '.join(missing)}")

    # API fields the module doesn't expose yet.
    covered = {option.get("api_field") for option in options.values()}
    for field_name, api_field in endpoint.fields.items():
        if field_name in covered or field_name in ignored or field_name in shared_options:
            continue
        if deprecated:
            context.report.add(INFO, name, f"API field '{field_name}' not added because the module is deprecated")
            continue
        option_name = option_name_for_field(api_field, context, options)
        if option_name is None or option_name in options:
            context.report.add(
                ERROR,
                name,
                f"API field '{field_name}' needs an option name that doesn't clash with existing options or with "
                "CONVERT_TO_ID/CONVERT_KEYS in utils.py. Add the option to the module config by hand "
                "or add the field to `ignore_api_fields`.",
            )
            continue
        version_added = None if is_new else context.next_version
        options[option_name] = managed_option(api_field, endpoint, version_added=version_added)
        if not is_new:
            context.report.add(INFO, name, f"added option '{option_name}' for new API field '{field_name}'")
    return config


def build_generated_tables(configs, context):
    """Build the lookup tables for generated.py from every module's options.

    Entries that already exist in the hand-written tables in utils.py are left out, because the hand-written
    entries win when utils.py merges the two.
    """
    hand = context.hand_tables
    endpoints_by_model = {endpoint.model: endpoint for endpoint in context.endpoints.values()}
    known_endpoints = {endpoint for endpoints in hand["API_APPS_ENDPOINTS"].values() for endpoint in endpoints}

    apps = {}
    for endpoint in sorted(context.endpoints.values(), key=lambda endpoint: endpoint.path):
        if endpoint.endpoint in known_endpoints:
            continue
        apps.setdefault(endpoint.app, []).append(endpoint.endpoint)
        known_endpoints.add(endpoint.endpoint)

    endpoint_names = {}
    allowed_query_params = {}
    for config in configs.values():
        endpoint = context.endpoints.get(config.get("api_path"))
        # Modules converted from hand-written ones have `lookup_fields: null` and use the hand-written tables.
        if endpoint is None or config.get("lookup_fields") is None:
            continue
        if not config["lookup_fields"]:
            context.report.add(
                WARNING,
                config["module"],
                "no lookup fields: the module finds existing objects by `id` only. Set `lookup_fields` in its config "
                "to fields that identify one object.",
            )
        if endpoint.endpoint not in hand["ENDPOINT_NAME_MAPPING"]:
            endpoint_names[endpoint.endpoint] = config["module"]
        endpoint_name = hand["ENDPOINT_NAME_MAPPING"].get(endpoint.endpoint, endpoint_names.get(endpoint.endpoint))
        if endpoint_name not in hand["ALLOWED_QUERY_PARAMS"]:
            option_names = []
            for field_name in config["lookup_fields"]:
                option_name = _option_for_api_field(config, field_name) or field_name
                option_names.append(option_name)
            allowed_query_params[endpoint_name] = sorted(option_names)

    # Foreign keys: map each option name to one target endpoint, but only when every module agrees on the target.
    targets = {}
    for config in configs.values():
        endpoint = context.endpoints.get(config.get("api_path"))
        if endpoint is None:
            continue
        for option_name, option in config["options"].items():
            api_field = endpoint.fields.get(option.get("api_field") or "")
            if not api_field or not api_field.related_model or api_field.content_type:
                targets.setdefault(option_name, set()).add(None)
                continue
            if not option.get("managed"):
                # Don't change how an existing hand-written option resolves its value.
                if option_name not in hand["CONVERT_TO_ID"]:
                    targets.setdefault(option_name, set()).add(None)
                continue
            target = endpoints_by_model.get(api_field.related_model)
            targets.setdefault(option_name, set()).add(target.endpoint if target else None)

    # ALLOWED_QUERY_PARAMS is also keyed by each module's own endpoint name (see run() in module_utils), so a
    # foreign key entry must not reuse one of those keys.
    module_lookup_keys = set(allowed_query_params)
    for config in configs.values():
        endpoint = context.endpoints.get(config.get("api_path"))
        if endpoint is not None:
            module_lookup_keys.add(
                hand["ENDPOINT_NAME_MAPPING"].get(endpoint.endpoint, endpoint_names.get(endpoint.endpoint))
            )

    convert_to_id = {}
    query_types = {}
    for option_name, target_names in sorted(targets.items()):
        if option_name in hand["CONVERT_TO_ID"] or len(target_names) != 1 or None in target_names:
            continue
        target_name = next(iter(target_names))
        target = next(endpoint for endpoint in context.endpoints.values() if endpoint.endpoint == target_name)
        convert_to_id[option_name] = target_name
        lookup = primary_lookup(target)
        if lookup and option_name not in hand["QUERY_TYPES"]:
            query_types[option_name] = lookup
        target_lookup = natural_key_fields(target)
        if target_lookup and option_name not in hand["ALLOWED_QUERY_PARAMS"] and option_name not in module_lookup_keys:
            allowed_query_params[option_name] = sorted(target_lookup)

    # Write-only API fields aren't returned by the API, so they can't be compared with the existing object.
    endpoint_write_only_fields = {}
    for config in configs.values():
        endpoint = context.endpoints.get(config.get("api_path"))
        if endpoint is None:
            continue
        for option in config["options"].values():
            api_field = endpoint.fields.get(option.get("api_field") or "")
            if option.get("managed") and api_field and api_field.write_only:
                endpoint_write_only_fields.setdefault(endpoint.endpoint, []).append(api_field.name)

    # Generated options renamed to avoid a clash are converted back to the API field name, per endpoint.
    endpoint_convert_keys = {}
    for config in configs.values():
        endpoint = context.endpoints.get(config.get("api_path"))
        if endpoint is None:
            continue
        for option_name, option in config["options"].items():
            if option.get("managed") and option.get("api_field") and option["api_field"] != option_name:
                endpoint_convert_keys.setdefault(endpoint.endpoint, {})[option_name] = option["api_field"]

    return {
        "API_APPS_ENDPOINTS": apps,
        "ENDPOINT_CONVERT_KEYS": dict(sorted(endpoint_convert_keys.items())),
        "ENDPOINT_WRITE_ONLY_FIELDS": {key: sorted(value) for key, value in sorted(endpoint_write_only_fields.items())},
        "ENDPOINT_NAME_MAPPING": dict(sorted(endpoint_names.items())),
        "CONVERT_TO_ID": convert_to_id,
        "QUERY_TYPES": query_types,
        "ALLOWED_QUERY_PARAMS": dict(sorted(allowed_query_params.items())),
    }


def check_foreign_keys(configs, generated, context):
    """Report options whose value would be looked up on a different endpoint than the API field points to."""
    hand = context.hand_tables
    endpoints_by_model = {endpoint.model: endpoint for endpoint in context.endpoints.values()}
    for config in configs.values():
        endpoint = context.endpoints.get(config.get("api_path"))
        if endpoint is None:
            continue
        for option_name, option in config["options"].items():
            api_field = endpoint.fields.get(option.get("api_field") or "")
            if not api_field or not api_field.related_model or api_field.content_type:
                continue
            target = endpoints_by_model.get(api_field.related_model)
            if target is None:
                continue
            lookup_endpoint = hand["CONVERT_TO_ID"].get(option_name, generated["CONVERT_TO_ID"].get(option_name))
            if lookup_endpoint is None:
                if option.get("managed"):
                    context.report.add(
                        WARNING,
                        config["module"],
                        f"option '{option_name}' can't be looked up by name, because another module uses the same "
                        "option name for something else. It accepts an ID or a dict of attributes.",
                    )
                continue
            lookup_app = context.find_app(lookup_endpoint, generated["API_APPS_ENDPOINTS"])
            if lookup_endpoint != target.endpoint or lookup_app != target.app:
                text = (
                    f"option '{option_name}' is looked up on '{lookup_app}.{lookup_endpoint}' (CONVERT_TO_ID) but "
                    f"the API field '{api_field.name}' points to '{target.app}.{target.endpoint}'"
                )
                if option.get("known_issue"):
                    context.report.add(WARNING, config["module"], f"{text} (known issue: {option['known_issue']})")
                else:
                    context.report.add(ERROR, config["module"], text)
