#!/usr/bin/env python3
"""Generate the collection's requirements.txt files from pyproject.toml.

`ansible-builder` resolves a collection's Python runtime dependencies from a
requirements.txt shipped inside the collection tarball. Two locations are needed:

  * ``meta/requirements.txt`` -- the standard location ``ansible-builder``
    discovers for any collection pulled into an Execution Environment.
  * ``requirements.txt`` at the collection root -- additionally required by Red
    Hat Automation Hub's certification tooling.

Both files are derived from pyproject.toml so it remains the single source of
truth for runtime versions. Neither is committed: both are gitignored and
regenerated at build/release time.

Every dependency under ``[tool.poetry.dependencies]`` is emitted except the
entries in ``EXCLUDED_DEPS``, so a newly added runtime dependency flows into the
requirements files automatically without touching this script.

The output uses floor-only specifiers (``>=X.Y.Z``): no ``==`` pins and no upper
caps, per Red Hat partner-engineering guidance (caps cause resolution conflicts
when multiple collections share an Execution Environment).
"""

from __future__ import annotations

from pathlib import Path

import tomllib

# Dependencies declared in pyproject.toml that must NOT be shipped in the EE
# requirements files. Everything else is emitted automatically, so pyproject.toml
# stays the single source of truth for what the collection needs at runtime.
EXCLUDED_DEPS = frozenset(
    {
        "python",  # interpreter constraint, not an installable package
        "ansible-core",  # provided by the EE base image; a collection must not pin it
        "asyncio",  # stdlib since Python 3.4; the PyPI backport breaks modern runtimes
    }
)

# Files to generate, relative to the repo root. Both ship in the tarball.
OUTPUT_FILES = ("requirements.txt", "meta/requirements.txt")


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


def requirement_lines(poetry_deps):
    """Return sorted ``name>=floor`` lines for every shippable runtime dependency.

    Args:
        poetry_deps (dict): The parsed `[tool.poetry.dependencies]` table.

    Returns:
        list[str]: One ``name>=X.Y.Z`` line per dependency not in
        ``EXCLUDED_DEPS``, sorted by name for stable, diff-friendly output.
    """
    lines = [f"{name}>={floor(spec)}" for name, spec in poetry_deps.items() if name not in EXCLUDED_DEPS]
    return sorted(lines)


def main():
    """Write the root and meta requirements files from `[tool.poetry.dependencies]`.

    Returns 0 on success.
    """
    project_root = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text())
    poetry_deps = pyproject["tool"]["poetry"]["dependencies"]

    lines = requirement_lines(poetry_deps)
    content = "\n".join(lines) + "\n"

    for rel_path in OUTPUT_FILES:
        out_path = project_root / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        print(f"Generated {out_path} with {len(lines)} deps:")
        for line in lines:
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
