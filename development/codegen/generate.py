"""Generate the collection's modules from the Nautobot REST API.

Usage (run from the repository root, normally through `invoke codegen`):

    python -m development.codegen.generate --schema openapi.json --metadata model_metadata.json [--check]

See development/codegen/README.md for how the pieces fit together.
"""

import argparse
import ast
import difflib
import importlib
import json
import re
import sys
from pathlib import Path

import jinja2
import yaml

from . import render, schema, sync
from .loader import COLLECTION_PACKAGE, REPO_ROOT, ensure_collection_importable

CODEGEN_DIR = Path(__file__).resolve().parent
MODULE_CONFIG_DIR = CODEGEN_DIR / "modules"
GLOBAL_CONFIG_PATH = CODEGEN_DIR / "config.yml"
MODULES_DIR = REPO_ROOT / "plugins" / "modules"
MODULE_UTILS_DIR = REPO_ROOT / "plugins" / "module_utils"
GENERATED_TABLES_PATH = MODULE_UTILS_DIR / "generated.py"

HAND_TABLE_NAMES = (
    "API_APPS_ENDPOINTS",
    "QUERY_TYPES",
    "CONVERT_TO_ID",
    "ENDPOINT_NAME_MAPPING",
    "ALLOWED_QUERY_PARAMS",
    "CONVERT_KEYS",
)

CONFIG_HEADER = (
    "# Module config for the code generator. The generator reads this file and rewrites it, so keep\n"
    "# comments out of it. See development/codegen/README.md.\n"
)


def read_hand_tables(utils_path=MODULE_UTILS_DIR / "utils.py"):
    """Return the hand-written lookup tables defined in utils.py, before the generated tables are merged in."""
    tree = ast.parse(Path(utils_path).read_text(encoding="utf-8"))
    tables = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in HAND_TABLE_NAMES:
                expression = compile(ast.Expression(node.value), str(utils_path), "eval")
                tables[name] = eval(expression, {"__builtins__": {}, "dict": dict, "set": set})  # noqa: S307  # pylint: disable=eval-used
    missing = set(HAND_TABLE_NAMES) - set(tables)
    if missing:
        raise ValueError(f"Couldn't find {', '.join(sorted(missing))} in {utils_path}")
    return tables


def shared_spec_options():
    """Return the option names defined by each shared argument spec in utils.py (`TAGS_ARG_SPEC` -> {"tags"})."""
    ensure_collection_importable()
    utils = importlib.import_module(f"{COLLECTION_PACKAGE}.plugins.module_utils.utils")
    return {name: set(getattr(utils, name)) for name in dir(utils) if name.endswith("_ARG_SPEC")}


def app_module_utils(app):
    """Return (module_utils module name, class name) for an app, such as ("ipam", "NautobotIpamModule")."""
    path = MODULE_UTILS_DIR / f"{app}.py"
    if not path.exists():
        return None
    match = re.search(r"^class (Nautobot\w+Module)\(NautobotModule\):", path.read_text(encoding="utf-8"), re.MULTILINE)
    return (app, match.group(1)) if match else None


def load_yaml(path):
    """Read a YAML file."""
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_module_configs():
    """Return every module config, keyed by module name."""
    return {path.stem: load_yaml(path) for path in sorted(MODULE_CONFIG_DIR.glob("*.yml"))}


def galaxy_version():
    """Return the collection version from galaxy.yml."""
    return load_yaml(REPO_ROOT / "galaxy.yml")["version"]


def render_documentation(config):
    """Return the DOCUMENTATION YAML for a module, with its options last."""
    documentation = dict(config["documentation"])
    options = {}
    for name, option in config["options"].items():
        if option.get("documentation") is not None:
            options[name] = option["documentation"]
    documentation["options"] = options
    # ansible-test's pep8 check allows lines up to 160 characters, including inside DOCUMENTATION.
    return render.to_yaml(documentation, width=140)


def _jinja_environment():
    environment = jinja2.Environment(  # noqa: S701 - generates Python source, not HTML
        loader=jinja2.FileSystemLoader(CODEGEN_DIR / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=jinja2.StrictUndefined,
    )
    environment.filters["to_python"] = render.to_python
    return environment


def render_module(config, environment=None):
    """Return the Python source for one module."""
    environment = environment or _jinja_environment()
    argument_spec = {
        name: option["argument_spec"]
        for name, option in config["options"].items()
        if option.get("argument_spec") is not None
    }
    kwargs = dict(config["ansible_module_kwargs"])
    # Long lists such as required_if read better as a variable, the way the hand-written modules did it.
    # AnsibleModule's documentation writes each rule as a tuple, but YAML stores it as a list, so convert each
    # rule back to a tuple.
    extra_kwargs = {
        name: [tuple(rule) if isinstance(rule, list) else rule for rule in kwargs.pop(name)]
        for name in list(kwargs)
        if name.startswith("required_")
    }
    source = environment.get_template("module.py.j2").render(
        config=config,
        documentation_yaml=render_documentation(config),
        argument_spec=argument_spec,
        extra_kwargs=extra_kwargs,
        module_call_arguments=", ".join(
            ["argument_spec=argument_spec"]
            + [f"{name}={render.to_python(value)}" for name, value in kwargs.items()]
            + [f"{name}={name}" for name in extra_kwargs]
        ),
    )
    return render.ruff_format(source, filename=f"plugins/modules/{config['module']}.py")


def render_generated_tables(tables, environment=None):
    """Return the Python source for plugins/module_utils/generated.py."""
    environment = environment or _jinja_environment()
    source = environment.get_template("generated.py.j2").render(tables=tables)
    return render.ruff_format(source, filename="plugins/module_utils/generated.py")


def render_config(config):
    """Return the YAML text of a module config."""
    return CONFIG_HEADER + render.to_yaml(config)


def build(schema_data, metadata, global_config=None, module_configs=None, hand_tables=None):
    """Run the generator in memory.

    Returns:
        (tuple): `files` (dict of path -> new content) and the `Report`.
    """
    global_config = global_config if global_config is not None else load_yaml(GLOBAL_CONFIG_PATH)
    module_configs = module_configs if module_configs is not None else load_module_configs()
    hand_tables = hand_tables if hand_tables is not None else read_hand_tables()

    endpoints = schema.parse_endpoints(schema_data, metadata)
    next_version = global_config.get("next_version") or sync.next_minor_version(galaxy_version())
    context = sync.Context(
        endpoints=endpoints,
        next_version=next_version,
        global_ignored_fields=set(global_config.get("ignore_api_fields") or {}),
        shared_spec_options=shared_spec_options(),
        hand_tables=hand_tables,
    )
    skip_endpoints = global_config.get("skip_endpoints") or {}
    hand_written = set(global_config.get("hand_written_modules") or {})

    configs = {}
    for name, config in module_configs.items():
        endpoint = endpoints.get(config["api_path"])
        if endpoint is None:
            context.report.add(sync.ERROR, name, f"endpoint {config['api_path']} isn't in the API schema")
            configs[name] = config
            continue
        configs[name] = sync.sync_module(config, endpoint, context)

    used_paths = {config["api_path"] for config in configs.values()}
    taken_names = set(configs) | hand_written | {path.stem for path in MODULES_DIR.glob("*.py")}
    for path, endpoint in sorted(endpoints.items()):
        if path in used_paths or not endpoint.creatable:
            continue
        if path in skip_endpoints:
            context.report.add(sync.INFO, path, f"skipped: {skip_endpoints[path]}")
            continue
        name = sync.module_name_for_endpoint(endpoint)
        if name in taken_names:
            context.report.add(
                sync.ERROR,
                path,
                f"new module name '{name}' is already taken. Add the endpoint to `skip_endpoints` "
                "or create its module config by hand.",
            )
            continue
        utils = app_module_utils(endpoint.app)
        if utils is None:
            context.report.add(
                sync.ERROR, path, f"no plugins/module_utils/{endpoint.app}.py with a Nautobot*Module class"
            )
            continue
        config = sync.new_module_config(name, endpoint, utils, next_version, set(context.shared_spec_options))
        configs[name] = sync.sync_module(config, endpoint, context, is_new=True)
        taken_names.add(name)
        context.report.add(sync.INFO, name, f"new module for {path}")

    for config in configs.values():
        endpoint = endpoints.get(config["api_path"])
        if endpoint is not None and "lookup_fields" not in config:
            config["lookup_fields"] = sync.natural_key_fields(endpoint)
        if endpoint is not None and config.get("generated_examples"):
            config["examples"] = sync.generate_examples(config, endpoint)

    tables = sync.build_generated_tables(configs, context)
    sync.check_foreign_keys(configs, tables, context)

    environment = _jinja_environment()
    files = {}
    for name, config in sorted(configs.items()):
        files[MODULE_CONFIG_DIR / f"{name}.yml"] = render_config(config)
        files[MODULES_DIR / f"{name}.py"] = render_module(config, environment)
    files[GENERATED_TABLES_PATH] = render_generated_tables(tables, environment)
    return files, context.report


def diff_files(files):
    """Return a unified diff between the files on disk and the generated content."""
    chunks = []
    for path, content in files.items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != content:
            relative = path.relative_to(REPO_ROOT)
            chunks.extend(
                difflib.unified_diff(
                    current.splitlines(keepends=True),
                    content.splitlines(keepends=True),
                    fromfile=f"a/{relative}",
                    tofile=f"b/{relative}",
                )
            )
    return "".join(chunks)


def write_files(files):
    """Write the files whose content changed and return their paths."""
    changed = []
    for path, content in files.items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            changed.append(path)
    return changed


def load_metadata(path):
    """Read model metadata saved either as plain JSON or as the raw output of dump_model_metadata.py."""
    text = Path(path).read_text(encoding="utf-8")
    if schema.BEGIN_MARKER in text:
        text = schema.extract_metadata_json(text)
    return json.loads(text)


def main(argv=None):
    """Run the generator from the command line and return the exit code."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--schema", required=True, help="OpenAPI schema JSON from `nautobot-server spectacular`")
    parser.add_argument("--metadata", required=True, help="Output of dump_model_metadata.py")
    parser.add_argument("--check", action="store_true", help="Don't write files; fail if they would change")
    parser.add_argument("--report", help="Also write the drift report to this file")
    args = parser.parse_args(argv)

    with open(args.schema, encoding="utf-8") as handle:
        schema_data = json.load(handle)
    files, report = build(schema_data, load_metadata(args.metadata))

    report_text = str(report)
    print(report_text or "No changes found in the API schema.")
    if args.report:
        Path(args.report).write_text(report_text + "\n", encoding="utf-8")

    exit_code = 1 if report.errors else 0
    if args.check:
        diff = diff_files(files)
        if diff:
            print("\nGenerated files are out of date. Run `invoke codegen` and commit the result.\n")
            print(diff)
            exit_code = 1
    else:
        for path in write_files(files):
            print(f"wrote {path.relative_to(REPO_ROOT)}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
