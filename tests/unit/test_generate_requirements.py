"""Tests for development/generate_requirements.py.

The script derives requirements.txt (root) and meta/requirements.txt from
pyproject.toml. Bugs in the version-spec parser or the dependency selection
would silently ship the wrong specifiers to consumers of the published
collection, so both are covered here.
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
    tests can call `floor()`, `requirement_lines()`, and `main()` directly.
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


class TestRequirementLines:
    def test_excludes_non_shippable_deps_and_sorts(self):
        poetry_deps = {
            "python": ">=3.11,<4.0",
            "ansible-core": ">=2.18,<2.20",
            "asyncio": "^3.4.3",
            "pynautobot": ">=3.0.0,<4.0.0",
            "requests": "^2.28.0",
            "netutils": "^1.2",
            "aiohttp": "^3.11.13",
        }
        assert generate_requirements.requirement_lines(poetry_deps) == [
            "aiohttp>=3.11.13",
            "netutils>=1.2",
            "pynautobot>=3.0.0",
            "requests>=2.28.0",
        ]

    def test_new_runtime_dep_flows_through_automatically(self):
        # A dependency added to pyproject that is not excluded is emitted with no
        # change to the script -- pyproject.toml stays the single source of truth.
        poetry_deps = {"python": ">=3.11,<4.0", "somenewlib": "^1.0.0"}
        assert generate_requirements.requirement_lines(poetry_deps) == ["somenewlib>=1.0.0"]

    def test_output_is_floor_only(self):
        # No `==` pins and no upper caps in any emitted line.
        poetry_deps = {"a": "^1.2.3", "b": ">=3.0.0,<4.0.0", "c": "~2.0"}
        for line in generate_requirements.requirement_lines(poetry_deps):
            assert ">=" in line
            assert "==" not in line
            assert "<" not in line


PYPROJECT_FIXTURE = """
[tool.poetry]
name = "x"
version = "0.0.1"

[tool.poetry.dependencies]
python = ">=3.11,<4.0"
ansible-core = ">=2.18,<2.20"
asyncio = "^3.4.3"
pynautobot = ">=3.0.0,<4.0.0"
requests = "^2.28.0"
netutils = "^1.2"
aiohttp = "^3.11.13"
"""

EXPECTED_LINES = [
    "aiohttp>=3.11.13",
    "netutils>=1.2",
    "pynautobot>=3.0.0",
    "requests>=2.28.0",
]


@pytest.fixture(name="project")
def project_fixture(tmp_path, monkeypatch):
    """A throwaway project root with a pyproject.toml the generator will read.

    `main()` locates the project root relative to the script's own path, so
    the module's `__file__` is pointed inside the temporary tree.
    """
    (tmp_path / "pyproject.toml").write_text(PYPROJECT_FIXTURE)
    (tmp_path / "development").mkdir()
    monkeypatch.setattr(generate_requirements, "__file__", str(tmp_path / "development" / "generate_requirements.py"))
    return tmp_path


class TestMain:
    def test_writes_both_requirements_files(self, project):
        assert generate_requirements.main([]) == 0

        root = (project / "requirements.txt").read_text().splitlines()
        meta = (project / "meta" / "requirements.txt").read_text().splitlines()
        assert root == EXPECTED_LINES
        assert meta == EXPECTED_LINES


class TestCheck:
    """`--check` is the CI drift gate: it must never write, and must fail on any mismatch."""

    def test_in_sync_passes(self, project, capsys):
        generate_requirements.main([])
        assert generate_requirements.main(["--check"]) == 0
        assert "in sync" in capsys.readouterr().out

    def test_missing_file_fails(self, project, capsys):
        assert generate_requirements.main(["--check"]) == 1
        err = capsys.readouterr().err
        assert "requirements.txt" in err
        assert "meta/requirements.txt" in err
        assert "invoke generate-requirements" in err
        # Check mode must not create the files it found missing.
        assert not (project / "requirements.txt").exists()
        assert not (project / "meta" / "requirements.txt").exists()

    def test_stale_file_fails_and_is_left_untouched(self, project, capsys):
        generate_requirements.main([])
        stale = project / "meta" / "requirements.txt"
        stale.write_text("pynautobot\n")

        assert generate_requirements.main(["--check"]) == 1
        err = capsys.readouterr().err
        assert "meta/requirements.txt" in err
        # Only the drifted file is reported, and it is not rewritten.
        assert err.splitlines()[0].endswith("meta/requirements.txt")
        assert stale.read_text() == "pynautobot\n"


class TestRealPyproject:
    """Guard rail: the real pyproject produces the expected EE requirement set.

    Notes are keyed off what plugins/extensions actually import: pynautobot,
    requests, netutils, and aiohttp. If a maintainer accidentally excludes one of
    those (or lets python/ansible-core/asyncio leak into the EE requirements),
    this fails.
    """

    IMPORTED_DEPS = {"pynautobot", "requests", "netutils", "aiohttp"}

    def _real_lines(self):
        import tomllib

        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
        return generate_requirements.requirement_lines(pyproject["tool"]["poetry"]["dependencies"])

    def test_imported_deps_are_emitted(self):
        names = {line.split(">=")[0] for line in self._real_lines()}
        assert self.IMPORTED_DEPS <= names

    def test_non_shippable_deps_are_excluded(self):
        names = {line.split(">=")[0] for line in self._real_lines()}
        assert names.isdisjoint(generate_requirements.EXCLUDED_DEPS)

    def test_all_lines_are_floor_only(self):
        for line in self._real_lines():
            assert ">=" in line
            assert "==" not in line
            assert "<" not in line
