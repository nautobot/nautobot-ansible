"""Turn Python data into YAML or Python source text with stable formatting."""

import json
import keyword
import re
import subprocess

import yaml


class _IndentedDumper(yaml.SafeDumper):
    """Indent list items under their parent key, the style used in the module DOCUMENTATION blocks."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


VERSION = re.compile(r"^\d+(\.\d+)+$")


def _represent_str(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if VERSION.match(data):
        # Ansible docs quote versions (version_added: "1.0.0") so YAML never reads them as numbers.
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def _represent_tuple(dumper, data):
    return dumper.represent_list(list(data))


_IndentedDumper.add_representer(str, _represent_str)
_IndentedDumper.add_representer(tuple, _represent_tuple)


def to_yaml(data, width=1_000_000):
    """Dump data as block-style YAML without sorting keys.

    Long strings are only wrapped when `width` is given. Wrapped plain strings load back unchanged.
    """
    return yaml.dump(
        data,
        Dumper=_IndentedDumper,
        sort_keys=False,
        width=width,
        allow_unicode=True,
        default_flow_style=False,
    )


def _is_identifier(key):
    return isinstance(key, str) and key.isidentifier() and not keyword.iskeyword(key)


def to_python(value):
    """Return Python source for a literal value, writing dicts with identifier keys as `dict(key=value)`."""
    if isinstance(value, dict):
        if all(_is_identifier(key) for key in value):
            return "dict(" + ", ".join(f"{key}={to_python(item)}" for key, item in value.items()) + ")"
        return "{" + ", ".join(f"{to_python(key)}: {to_python(item)}" for key, item in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ", ".join(to_python(item) for item in value) + "]"
    if isinstance(value, tuple):
        if len(value) == 1:
            return f"({to_python(value[0])},)"
        return "(" + ", ".join(to_python(item) for item in value) + ")"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if value is None or isinstance(value, (bool, int, float)):
        return repr(value)
    raise TypeError(f"Can't write {value!r} as a Python literal")


def ruff_format(source, filename="generated.py"):
    """Sort imports and format Python source with ruff, the same way `invoke autoformat` does."""
    sorted_source = subprocess.run(  # noqa: S603
        ["ruff", "check", "--select", "I", "--fix", "--quiet", "--stdin-filename", filename, "-"],  # noqa: S607
        input=source,
        capture_output=True,
        text=True,
        check=False,
    )
    if sorted_source.returncode not in (0, 1):
        raise RuntimeError(f"ruff check failed for {filename}:\n{sorted_source.stderr}")
    formatted = subprocess.run(  # noqa: S603
        ["ruff", "format", "--quiet", "--stdin-filename", filename, "-"],  # noqa: S607
        input=sorted_source.stdout,
        capture_output=True,
        text=True,
        check=False,
    )
    if formatted.returncode != 0:
        raise RuntimeError(f"ruff format failed for {filename}:\n{formatted.stderr}")
    return formatted.stdout
