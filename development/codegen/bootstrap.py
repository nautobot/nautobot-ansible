"""Create module configs from the hand-written modules that existed before the code generator.

This was run once, when the generator was introduced. It is kept so the conversion can be reviewed and repeated:

    python -m development.codegen.bootstrap --schema openapi.json --metadata model_metadata.json

Modules listed under `hand_written_modules` in config.yml are skipped.
"""

import argparse
import ast
import json
import sys
from pathlib import Path

from . import schema
from .generate import (
    GLOBAL_CONFIG_PATH,
    MODULE_CONFIG_DIR,
    MODULE_UTILS_DIR,
    MODULES_DIR,
    load_metadata,
    load_yaml,
    render_config,
)
from .inspect_module import inspect_module


def _find_endpoint(info, endpoints):
    candidates = [endpoint for endpoint in endpoints.values() if endpoint.endpoint == info["endpoint"]]
    if len(candidates) > 1:
        candidates = [endpoint for endpoint in candidates if endpoint.app == info["utils_module"]]
    if len(candidates) != 1:
        raise ValueError(f"Can't find a single API endpoint for {info['name']} ({info['endpoint']})")
    return candidates[0]


def _api_field(option_name, spec, endpoint, convert_keys):
    if option_name in endpoint.fields:
        return option_name
    if convert_keys.get(option_name) in endpoint.fields:
        return convert_keys[option_name]
    for alias in (spec or {}).get("aliases", []):
        if alias in endpoint.fields:
            return alias
    return None


def module_config_from_file(path, endpoints, convert_keys):
    """Return the module config that reproduces an existing module file."""
    info = inspect_module(path)
    endpoint = _find_endpoint(info, endpoints)
    documentation = dict(info["documentation"])
    doc_options = documentation.pop("options", None) or {}

    options = {}
    for name, spec in info["argument_spec"].items():
        options[name] = {"api_field": None, "argument_spec": spec, "documentation": doc_options.get(name)}
    for name, doc in doc_options.items():
        if name not in options:
            options[name] = {"api_field": None, "argument_spec": None, "documentation": doc}
    for name, option in options.items():
        option["api_field"] = _api_field(name, option["argument_spec"], endpoint, convert_keys)
        if option["argument_spec"] is None:
            del option["argument_spec"]
        if option["documentation"] is None:
            del option["documentation"]

    return {
        "module": info["name"],
        "api_path": endpoint.path,
        "endpoint": endpoint.endpoint,
        "header": info["header"],
        "utils_module": info["utils_module"],
        "class_name": info["class_name"],
        "endpoint_constant": info["endpoint_constant"],
        "instance_var": info["instance_var"],
        "instance_kwargs": info["instance_kwargs"],
        "main_docstring": info["main_docstring"],
        "shared_specs": info["shared_specs"],
        "ansible_module_kwargs": info["ansible_module_kwargs"],
        "extra_imports": info["extra_imports"],
        "post_module_code": info["post_module_code"],
        "ignore_api_fields": {},
        "lookup_fields": None,
        "generated_examples": False,
        "options": options,
        "documentation": documentation,
        "examples": info["examples"],
        "return": info["return"],
    }


def main(argv=None):
    """Write a module config for every hand-written module that isn't listed in `hand_written_modules`."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--metadata", required=True)
    args = parser.parse_args(argv)

    with open(args.schema, encoding="utf-8") as handle:
        endpoints = schema.parse_endpoints(json.load(handle), load_metadata(args.metadata))
    global_config = load_yaml(GLOBAL_CONFIG_PATH)
    hand_written = set(global_config.get("hand_written_modules") or {})
    convert_keys = read_convert_keys()

    MODULE_CONFIG_DIR.mkdir(exist_ok=True)
    for path in sorted(MODULES_DIR.glob("*.py")):
        if path.name == "__init__.py" or path.stem in hand_written:
            continue
        config = module_config_from_file(path, endpoints, convert_keys)
        Path(MODULE_CONFIG_DIR / f"{path.stem}.yml").write_text(render_config(config), encoding="utf-8")
        print(f"wrote {path.stem}.yml")
    return 0


def read_convert_keys():
    """Return CONVERT_KEYS from utils.py, which maps option names to the API field names they're sent as."""
    utils_path = MODULE_UTILS_DIR / "utils.py"
    for node in ast.parse(utils_path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "CONVERT_KEYS":
            return ast.literal_eval(node.value)
    return {}


if __name__ == "__main__":
    sys.exit(main())
