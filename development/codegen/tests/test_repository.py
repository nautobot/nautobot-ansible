"""Tests that check the generated files committed to the repository.

These don't need a Nautobot schema: they check that the committed modules match their configs and that each
generated module documents the options it accepts.
"""

import pytest

from development.codegen import generate
from development.codegen.compare import compare_main, compare_modules
from development.codegen.loader import load_module_file, load_module_source

MODULE_CONFIGS = generate.load_module_configs()
GLOBAL_CONFIG = generate.load_yaml(generate.GLOBAL_CONFIG_PATH)


def test_every_module_is_generated_or_listed_as_hand_written():
    hand_written = set(GLOBAL_CONFIG["hand_written_modules"])
    modules = {path.stem for path in generate.MODULES_DIR.glob("*.py") if path.name != "__init__.py"}
    assert modules == set(MODULE_CONFIGS) | hand_written
    assert not hand_written & set(MODULE_CONFIGS)


@pytest.mark.parametrize("name", sorted(MODULE_CONFIGS))
def test_module_file_matches_its_config(name):
    """Someone edited the module instead of its config, or forgot to run `invoke codegen`."""
    expected = generate.render_module(MODULE_CONFIGS[name])
    assert (generate.MODULES_DIR / f"{name}.py").read_text() == expected


@pytest.mark.parametrize("name", sorted(MODULE_CONFIGS))
def test_config_file_is_in_generator_format(name):
    path = generate.MODULE_CONFIG_DIR / f"{name}.yml"
    assert path.read_text() == generate.render_config(MODULE_CONFIGS[name])


@pytest.mark.parametrize("name", sorted(MODULE_CONFIGS))
def test_module_documents_its_options(name):
    """Every module-specific option has documentation, with the same type, choices and elements."""
    loaded = load_module_file(generate.MODULES_DIR / f"{name}.py")
    documented = loaded["documentation"]["options"]
    for option_name, option in MODULE_CONFIGS[name]["options"].items():
        spec = option.get("argument_spec")
        if spec is None:
            continue
        assert option_name in documented, f"{option_name} isn't documented"
        doc = documented[option_name]
        if not option.get("managed"):
            continue
        assert doc["type"] == spec["type"]
        assert doc.get("choices") == spec.get("choices")
        assert doc.get("elements") == spec.get("elements")


def test_generated_lookup_tables_match_the_committed_file():
    """Check that generated.py runs, defines its tables as dicts, and repeats no hand-written CONVERT_TO_ID key."""
    namespace = {}
    exec(compile(generate.GENERATED_TABLES_PATH.read_text(), "generated.py", "exec"), namespace)  # noqa: S102
    for name in ("API_APPS_ENDPOINTS", "ENDPOINT_CONVERT_KEYS", "ENDPOINT_NAME_MAPPING", "CONVERT_TO_ID"):
        assert isinstance(namespace[f"GENERATED_{name}"], dict)
    hand = generate.read_hand_tables()
    for key in namespace["GENERATED_CONVERT_TO_ID"]:
        assert key not in hand["CONVERT_TO_ID"], f"{key} is in both the hand-written and generated CONVERT_TO_ID"


def test_compare_modules_reports_changes():
    source = generate.MODULES_DIR.joinpath("tag.py").read_text()
    old = load_module_source(source, "tag")
    new = load_module_source(source.replace('version_added: "1.0.0"', 'version_added: "1.1.0"', 1), "tag")
    new["ansible_module_kwargs"]["argument_spec"]["extra"] = {"type": "str"}

    differences = compare_modules(old, new)

    assert "argument_spec: added option 'extra' {'type': 'str'}" in differences
    assert any(difference.startswith("DOCUMENTATION: changed") for difference in differences)
    assert compare_modules(old, load_module_source(source, "tag")) == []


def test_read_hand_tables_ignores_the_generated_entries():
    hand = generate.read_hand_tables()
    assert hand["CONVERT_TO_ID"]["group"] == "tenant_groups"
    assert "cable_type" not in hand["CONVERT_TO_ID"]


def test_compare_main_reports_dropped_module_class_arguments():
    """The generator once dropped `remove_keys=[...]`; compare.py must notice that kind of change."""
    source = generate.MODULES_DIR.joinpath("prefix.py").read_text(encoding="utf-8")
    assert 'remove_keys=["first_available"]' in source
    changed = source.replace(', remove_keys=["first_available"]', "")

    assert compare_main(source, source) == []
    assert compare_main(source, changed) == [
        "main(): statements after AnsibleModule() changed (for example the module class arguments)"
    ]


def test_module_class_arguments_come_from_the_config():
    config = MODULE_CONFIGS["device_interface"]
    assert config["instance_kwargs"] == {"remove_keys": ["update_vc_child"]}
    assert 'remove_keys=["update_vc_child"]' in generate.render_module(config)
