"""Tests for templating of the token and api_endpoint inventory options."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback

import pytest
import yaml
from ansible.errors import AnsibleError
from ansible.inventory.data import InventoryData
from ansible.parsing.dataloader import DataLoader
from ansible.plugins import AnsiblePlugin
from ansible.plugins.loader import init_plugin_loader, inventory_loader

init_plugin_loader()

PLUGINS = ["networktocode.nautobot.inventory", "networktocode.nautobot.gql_inventory"]
SECRET = "SEKRIT-must-never-appear"


@pytest.fixture(params=PLUGINS)
def run_parse(request, tmp_path, monkeypatch):
    """Parse an inventory file with the given options, without contacting Nautobot."""
    monkeypatch.delenv("NAUTOBOT_URL", raising=False)
    monkeypatch.delenv("NAUTOBOT_TOKEN", raising=False)

    def _run(**options):
        path = tmp_path / "nautobot.yml"
        path.write_text(yaml.safe_dump({"plugin": request.param, **options}))
        plugin = inventory_loader.get(request.param)
        monkeypatch.setattr(plugin, "main", lambda: None)
        plugin.parse(InventoryData(), DataLoader(), str(path), cache=False)
        return plugin

    return _run


def full_error_text(exc):
    """The error as a traceback would print it, including any chained causes."""
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


def test_plain_token_is_used_unchanged(run_parse):
    plugin = run_parse(api_endpoint="http://localhost:8000", token="1234567890abcdef")

    assert plugin.headers["Authorization"] == "Token 1234567890abcdef"


def test_templated_token_is_rendered(run_parse, monkeypatch):
    monkeypatch.setenv("TEST_NB_TOKEN", "token-from-lookup")

    plugin = run_parse(
        api_endpoint="http://localhost:8000", token="{{ lookup('ansible.builtin.env', 'TEST_NB_TOKEN') }}"
    )

    assert plugin.headers["Authorization"] == "Token token-from-lookup"


def test_templated_api_endpoint_is_rendered(run_parse, monkeypatch):
    monkeypatch.setenv("TEST_NB_URL", "http://nautobot.example.com/")

    plugin = run_parse(api_endpoint="{{ lookup('ansible.builtin.env', 'TEST_NB_URL') }}", token="abc")

    assert plugin.api_endpoint == "http://nautobot.example.com"


def test_token_from_the_environment_still_works(run_parse, monkeypatch):
    monkeypatch.setenv("NAUTOBOT_TOKEN", "token-from-env")

    plugin = run_parse(api_endpoint="http://localhost:8000")

    assert plugin.headers["Authorization"] == "Token token-from-env"


@pytest.mark.parametrize(
    "template, expected",
    [
        ("{{ ('0123456789abcdef' * 3)[:40] }}", "0123456789abcdef0123456789abcdef01234567"),
        ("{{ 'a' * 40 }}", "a" * 40),
    ],
)
def test_templated_token_from_the_environment_is_rendered(run_parse, monkeypatch, template, expected):
    monkeypatch.setenv("NAUTOBOT_TOKEN", template)

    plugin = run_parse(api_endpoint="http://localhost:8000")

    assert plugin.headers["Authorization"] == f"Token {expected}"


def test_templated_api_endpoint_from_the_environment_is_rendered(run_parse, monkeypatch):
    monkeypatch.setenv("NAUTOBOT_URL", "{{ 'http://nautobot.example.com/' }}")

    plugin = run_parse(token="abc")

    assert plugin.api_endpoint == "http://nautobot.example.com"


def test_untrusted_templated_token_is_rendered(run_parse, monkeypatch):
    # ansible-core 2.19+ only renders strings trusted as templates. Encoding and
    # decoding drops that trust, as for a value from a source Ansible doesn't trust.
    get_option = AnsiblePlugin.get_option

    def get_untrusted_option(self, option, hostvars=None):
        value = get_option(self, option, hostvars)
        return value.encode().decode() if isinstance(value, str) else value

    monkeypatch.setattr(AnsiblePlugin, "get_option", get_untrusted_option)

    plugin = run_parse(api_endpoint="http://localhost:8000", token="{{ 'a' * 40 }}")

    assert plugin.headers["Authorization"] == f"Token {'a' * 40}"


def test_failed_token_template_names_the_option(run_parse):
    with pytest.raises(AnsibleError, match="token"):
        run_parse(api_endpoint="http://localhost:8000", token="{{ lookup('no_such_lookup_plugin_xyz') }}")


def test_failed_token_template_does_not_leak_the_secret(run_parse, monkeypatch):
    # The template fails after the secret is fetched, with an error that quotes
    # the value it choked on.
    monkeypatch.setenv("TEST_NB_SECRET", SECRET)

    with pytest.raises(AnsibleError, match="token") as excinfo:
        run_parse(
            api_endpoint="http://localhost:8000",
            token="{{ lookup('ansible.builtin.env', 'TEST_NB_SECRET') | to_datetime }}",
        )

    assert SECRET not in full_error_text(excinfo.value)
