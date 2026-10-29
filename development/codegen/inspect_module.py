"""Read the structure of an existing hand-written module.

`bootstrap.py` uses this to turn the modules that existed before the code generator into module config files.
"""

import ast
import importlib
from pathlib import Path

from .loader import COLLECTION_PACKAGE, ensure_collection_importable, load_module_source

UTILS_MODULE = f"{COLLECTION_PACKAGE}.plugins.module_utils.utils"


def _header_lines(source):
    """Return the comment lines between the shebang/coding lines and `from __future__`."""
    lines = []
    for line in source.splitlines():
        if line.startswith("from __future__"):
            break
        if line.startswith("#!") or line.startswith("# -*- coding"):
            continue
        if line.startswith("#"):
            lines.append(line)
    return lines


def _main_function(tree):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            return node
    raise ValueError("No main() function found")


def _shared_specs(main):
    """Return the names passed to `deepcopy()` in main(), in order (for example `NAUTOBOT_ARG_SPEC`)."""
    names = []
    for node in ast.walk(main):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "deepcopy":
            if node.args and isinstance(node.args[0], ast.Name):
                names.append(node.args[0].id)
    # ast.walk is breadth-first; sort by position in the source instead.
    positions = {}
    for node in ast.walk(main):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "deepcopy":
            if node.args and isinstance(node.args[0], ast.Name):
                positions.setdefault(node.args[0].id, (node.lineno, node.col_offset))
    return sorted(set(names), key=lambda name: positions[name])


def _module_utils_import(tree):
    """Return (module_utils module name, class name, endpoint constant name) used by the module."""
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        if not node.module.startswith(f"{COLLECTION_PACKAGE}.plugins.module_utils."):
            continue
        utils_module = node.module.rsplit(".", 1)[-1]
        if utils_module == "utils":
            continue
        names = [alias.name for alias in node.names]
        class_names = [name for name in names if name.startswith("Nautobot")]
        constants = [name for name in names if name.startswith("NB_")]
        return utils_module, class_names[0] if class_names else None, constants[0] if constants else None
    return None, None, None


def instance_kwargs(main):
    """Return the keyword arguments passed to the Nautobot*Module class in main(), such as `remove_keys`."""
    for node in ast.walk(main):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "").startswith("Nautobot"):
            return {keyword.arg: ast.literal_eval(keyword.value) for keyword in node.keywords}
    return {}


def _instance_statements(main):
    """Split main() into the AnsibleModule assignment, the statements after it, and the instance variable name."""
    body = main.body
    module_index = None
    for index, node in enumerate(body):
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and getattr(node.value.func, "id", None) == "AnsibleModule"
        ):
            module_index = index
            break
    if module_index is None:
        return None, [], None
    instance_var = None
    post_module = []
    for node in body[module_index + 1 :]:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and getattr(node.value.func, "id", "").startswith("Nautobot")
        ):
            instance_var = node.targets[0].id
            break
        post_module.append(node)
    return body[module_index], post_module, instance_var


def _extra_imports(tree):
    """Return the module names from every top-level `import x` statement."""
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
    return imports


def inspect_module(path):
    """Return a dict describing an existing module file."""
    ensure_collection_importable()
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    main = _main_function(tree)
    loaded = load_module_source(source, name=path.stem)
    kwargs = dict(loaded["ansible_module_kwargs"] or {})

    utils_module, class_name, constant = _module_utils_import(tree)
    endpoint = None
    if utils_module and constant:
        app_utils = importlib.import_module(f"{COLLECTION_PACKAGE}.plugins.module_utils.{utils_module}")
        endpoint = getattr(app_utils, constant)

    shared_specs = _shared_specs(main)
    utils = importlib.import_module(UTILS_MODULE)
    shared = {}
    for name in shared_specs:
        shared.update(getattr(utils, name))

    argument_spec = kwargs.pop("argument_spec", {})
    module_spec = {name: spec for name, spec in argument_spec.items() if name not in shared or shared[name] != spec}

    main_docstring = ast.get_docstring(main, clean=False)
    _, post_module, instance_var = _instance_statements(main)
    return {
        "name": path.stem,
        "header": _header_lines(source),
        "documentation": loaded["documentation"],
        "examples": loaded["examples"],
        "return": loaded["return"],
        "utils_module": utils_module,
        "class_name": class_name,
        "endpoint_constant": constant,
        "endpoint": endpoint,
        "shared_specs": shared_specs,
        "argument_spec": module_spec,
        "ansible_module_kwargs": kwargs,
        "main_docstring": main_docstring,
        "instance_var": instance_var,
        "instance_kwargs": instance_kwargs(main),
        "post_module_code": [ast.get_source_segment(source, node) for node in post_module],
        "extra_imports": _extra_imports(tree),
    }
