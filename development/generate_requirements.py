#!/usr/bin/env python3
"""Generate the collection's root requirements.txt from pyproject.toml.

Red Hat Automation Hub's `ansible-builder` reads a root-level
requirements.txt to install the collection's Python runtime deps when
building an Execution Environment. We don't commit this file because
pyproject.toml is the single source of truth for runtime versions --
this script derives requirements.txt from it on demand (build/release).

The output uses floor-only specifiers (>=X.Y.Z); no `==` pins, no
upper caps, per Red Hat partner-engineering guidance (caps cause
conflicts when multiple collections share an EE).
"""

from __future__ import annotations

import sys
from pathlib import Path

import tomllib

# Runtime deps directly imported by plugin/extension code (verified via grep).
# Update this list if a new direct import is added; CI should keep it honest.
EE_DEPS = [
    "pynautobot",  # plugins/action/*, plugins/lookup/*
    "requests",  # plugins/action/{query_graphql,graphql_info,graphql_facts}.py
    "netutils",  # plugins/inventory/gql_inventory.py
    "aiohttp",  # extensions/eda/plugins/event_source/nautobot_changelog.py
]


def floor(spec):
    """Return the minimum version from a Poetry constraint string.

    Handles `^1.2.3`, `~1.2.3`, `>=1.2.3,<2.0.0`, plain `1.2.3`.
    Raises if no floor can be determined.
    """
    if isinstance(spec, dict):
        spec = spec.get("version", "")
    spec = spec.strip()
    if not spec:
        raise ValueError("empty version spec")
    if spec.startswith(("^", "~")):
        return spec[1:].strip()
    for part in spec.split(","):
        part = part.strip()
        if part.startswith(">="):
            return part[2:].strip()
    if spec[0].isdigit():
        return spec
    raise ValueError(f"cannot derive floor from spec: {spec!r}")


def main():
    """Write requirements.txt at the repo root from `[tool.poetry.dependencies]` floors.

    Returns 0 on success, 1 if any name in `EE_DEPS` is missing from pyproject.toml.
    """
    project_root = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text())
    poetry_deps = pyproject["tool"]["poetry"]["dependencies"]

    lines = []
    for name in EE_DEPS:
        if name not in poetry_deps:
            print(f"ERROR: '{name}' is required in EE_DEPS but missing from pyproject.toml", file=sys.stderr)
            return 1
        lines.append(f"{name}>={floor(poetry_deps[name])}")

    out_path = project_root / "requirements.txt"
    out_path.write_text("\n".join(lines) + "\n")
    print(f"Generated {out_path} with {len(lines)} deps:")
    for line in lines:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
