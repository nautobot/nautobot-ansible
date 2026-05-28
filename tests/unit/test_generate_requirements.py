"""Tests for development/generate_requirements.py.

The script derives the root requirements.txt from pyproject.toml. Bugs in
the version-spec parser would silently ship the wrong floor to consumers
of the published collection -- so the parsing is covered exhaustively.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "development" / "generate_requirements.py"

# `development/` is in galaxy.yml's build_ignore, so the script isn't present
# when ansible-test units runs against the installed collection tarball. Skip
# the whole module in that context; the script is dev tooling, not collection
# runtime, and is covered by `poetry run pytest` against the source tree.
pytestmark = pytest.mark.skipif(
    not SCRIPT_PATH.is_file(),
    reason="development/generate_requirements.py not available (collection-install context)",
)


def _load_module():
    """Load development/generate_requirements.py as a Python module.

    The file isn't a package member so we import it via importlib so the
    tests can call `floor()` and `main()` directly.
    """
    spec = importlib.util.spec_from_file_location("generate_requirements", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["generate_requirements"] = module
    spec.loader.exec_module(module)
    return module


if SCRIPT_PATH.is_file():
    generate_requirements = _load_module()
    floor = generate_requirements.floor
else:
    generate_requirements = None
    floor = None


class TestFloor:
    @pytest.mark.parametrize(
        "spec,expected",
        [
            ("^1.2.3", "1.2.3"),
            ("^1.2", "1.2"),
            ("^0.1.0", "0.1.0"),
            ("~1.2.3", "1.2.3"),
            (">=1.2.3,<2.0.0", "1.2.3"),
            (">=3.0.0,<4.0.0", "3.0.0"),
            (">=2.28.0", "2.28.0"),
            (">= 2.28.0", "2.28.0"),
            ("1.2.3", "1.2.3"),
            ("  ^1.2.3  ", "1.2.3"),
        ],
    )
    def test_string_specs(self, spec, expected):
        assert floor(spec) == expected

    @pytest.mark.parametrize(
        "spec,expected",
        [
            ({"version": "^1.2.3"}, "1.2.3"),
            ({"version": ">=3.0.0,<4.0.0", "python": ">=3.10"}, "3.0.0"),
            ({"version": ">=2.28.0"}, "2.28.0"),
            ({"version": "1.0"}, "1.0"),
        ],
    )
    def test_dict_specs(self, spec, expected):
        assert floor(spec) == expected

    @pytest.mark.parametrize(
        "spec",
        [
            "",
            "   ",
            "*",
            "latest",
            "any",
        ],
    )
    def test_invalid_specs_raise(self, spec):
        with pytest.raises(ValueError):
            floor(spec)

    def test_dict_without_version_raises(self):
        with pytest.raises(ValueError):
            floor({"python": ">=3.10"})


class TestMain:
    def test_writes_expected_lines_to_requirements_txt(self, tmp_path, monkeypatch):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            """
[tool.poetry]
name = "x"
version = "0.0.1"

[tool.poetry.dependencies]
python = ">=3.11,<4.0"
pynautobot = ">=3.0.0,<4.0.0"
requests = "^2.28.0"
netutils = "^1.2"
aiohttp = "^3.11.13"
"""
        )

        monkeypatch.setattr(
            generate_requirements, "__file__", str(tmp_path / "development" / "generate_requirements.py")
        )
        (tmp_path / "development").mkdir()

        rc = generate_requirements.main()
        assert rc == 0

        produced = (tmp_path / "requirements.txt").read_text().splitlines()
        assert produced == [
            "pynautobot>=3.0.0",
            "requests>=2.28.0",
            "netutils>=1.2",
            "aiohttp>=3.11.13",
        ]

    def test_returns_nonzero_when_ee_dep_missing(self, tmp_path, monkeypatch, capsys):
        pyproject = tmp_path / "pyproject.toml"
        # `requests` is in EE_DEPS but absent from this synthetic pyproject.
        pyproject.write_text(
            """
[tool.poetry]
name = "x"
version = "0.0.1"

[tool.poetry.dependencies]
python = ">=3.11,<4.0"
pynautobot = ">=3.0.0,<4.0.0"
netutils = "^1.2"
aiohttp = "^3.11.13"
"""
        )

        monkeypatch.setattr(
            generate_requirements, "__file__", str(tmp_path / "development" / "generate_requirements.py")
        )
        (tmp_path / "development").mkdir()

        rc = generate_requirements.main()
        assert rc == 1
        err = capsys.readouterr().err
        assert "requests" in err
        assert not (tmp_path / "requirements.txt").exists()


class TestEEDepsAllowlist:
    """Guard rails: the EE_DEPS list reflects what the collection actually imports.

    If this assertion fails it means a maintainer changed EE_DEPS without updating the
    comment that documents the source-of-truth grep, or the script's allowlist drifted
    from what plugins/extensions actually import.
    """

    EXPECTED = {"pynautobot", "requests", "netutils", "aiohttp"}

    def test_allowlist_matches_documented_set(self):
        assert set(generate_requirements.EE_DEPS) == self.EXPECTED
