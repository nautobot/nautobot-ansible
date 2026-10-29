"""Compare module interfaces between a git ref and the working tree.

Prints, for each module, the options that were added, removed or changed, and whether DOCUMENTATION, EXAMPLES,
RETURN, the other AnsibleModule arguments, or the rest of main() changed. Formatting-only changes are ignored.

    python -m development.codegen.compare --ref origin/develop
"""

import argparse
import ast
import subprocess
import sys

from .loader import REPO_ROOT, load_module_source


def normalize(value):
    """Convert tuples to lists so `("a", "b")` and `["a", "b"]` compare equal, as they do for AnsibleModule."""
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    return value


def compare_modules(old, new):
    """Return a list of human-readable differences between two loaded modules (see loader.load_module_source)."""
    differences = []
    old_kwargs = normalize(old["ansible_module_kwargs"] or {})
    new_kwargs = normalize(new["ansible_module_kwargs"] or {})
    old_spec = old_kwargs.pop("argument_spec", {})
    new_spec = new_kwargs.pop("argument_spec", {})
    for name in sorted(set(old_spec) | set(new_spec)):
        if name not in new_spec:
            differences.append(f"argument_spec: removed option '{name}'")
        elif name not in old_spec:
            differences.append(f"argument_spec: added option '{name}' {new_spec[name]}")
        elif old_spec[name] != new_spec[name]:
            differences.append(f"argument_spec: changed option '{name}': {old_spec[name]} -> {new_spec[name]}")
    if old_kwargs != new_kwargs:
        differences.append(f"AnsibleModule arguments changed: {old_kwargs} -> {new_kwargs}")

    old_doc = dict(old["documentation"])
    new_doc = dict(new["documentation"])
    old_options = old_doc.pop("options", {}) or {}
    new_options = new_doc.pop("options", {}) or {}
    for name in sorted(set(old_options) | set(new_options)):
        if name not in new_options:
            differences.append(f"DOCUMENTATION: removed option '{name}'")
        elif name not in old_options:
            differences.append(f"DOCUMENTATION: added option '{name}'")
        elif old_options[name] != new_options[name]:
            differences.append(f"DOCUMENTATION: changed option '{name}'")
    if old_doc != new_doc:
        changed = sorted(key for key in set(old_doc) | set(new_doc) if old_doc.get(key) != new_doc.get(key))
        differences.append(f"DOCUMENTATION: changed {', '.join(changed)}")
    if old["examples"] != new["examples"]:
        differences.append("EXAMPLES changed")
    if old["return"] != new["return"]:
        differences.append("RETURN changed")
    return differences


def main_structure(source):
    """Return the parts of a module's main() that the generator writes, as comparable AST dumps.

    The argument spec isn't included because `compare_modules` checks it with the real values.
    """
    tree = ast.parse(source)
    main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    imports = sorted(alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names)
    statements = []
    after_module = False
    for node in main.body:
        is_call = isinstance(node, (ast.Assign, ast.Expr)) and isinstance(node.value, ast.Call)
        if is_call and getattr(node.value.func, "id", None) == "AnsibleModule":
            after_module = True
            continue
        if after_module:
            # The class constructor call, its run() call, and any statements in between.
            statements.append(ast.dump(node.value if isinstance(node, ast.Assign) else node))
    return {"imports": imports, "statements_after_ansible_module": statements}


def compare_main(old_source, new_source):
    """Return differences in main() after the AnsibleModule is created, and in the plain imports."""
    old = main_structure(old_source)
    new = main_structure(new_source)
    differences = []
    if old["imports"] != new["imports"]:
        differences.append(f"imports changed: {old['imports']} -> {new['imports']}")
    if old["statements_after_ansible_module"] != new["statements_after_ansible_module"]:
        differences.append("main(): statements after AnsibleModule() changed (for example the module class arguments)")
    return differences


def _git_show(ref, path):
    result = subprocess.run(  # noqa: S603
        ["git", "show", f"{ref}:{path}"],  # noqa: S607
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def main(argv=None):
    """Print the interface differences of every module."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", default="origin/develop", help="git ref to compare the working tree with")
    args = parser.parse_args(argv)

    modules_dir = REPO_ROOT / "plugins" / "modules"
    changed = 0
    for path in sorted(modules_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        new = load_module_source(path.read_text(encoding="utf-8"), name=path.stem)
        old_source = _git_show(args.ref, f"plugins/modules/{path.name}")
        if old_source is None:
            print(f"{path.stem}: new module")
            changed += 1
            continue
        new_source = path.read_text(encoding="utf-8")
        differences = compare_modules(load_module_source(old_source, name=path.stem), new)
        differences += compare_main(old_source, new_source)
        if differences:
            changed += 1
            print(f"{path.stem}:")
            for difference in differences:
                print(f"  {difference}")
    print(f"{changed} module(s) differ from {args.ref}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
