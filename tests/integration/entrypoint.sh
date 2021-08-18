#!/bin/bash -eu

#########################################
# Docker entrypoint for integration tests
#
# This probably is usable locally in a native setup, but it isn't recommended.
# You should manually configure `integration_config.yml` instead and then run
# your tests.

set -o pipefail

function render {
  readonly template="$1"; shift
  readonly content="$(cat "$template")"

  eval "echo \"$content\""
}

function main {
    echo
    echo "# Running integration tests..."
    echo

    echo "# Rendering integration configuration"
    render "./tests/integration/integration_config.tmpl.yml" > ./tests/integration/integration_config.yml

    echo "# Checking to make sure Nautobot server is reachable.."
    timeout 300 bash -c 'while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' nautobot:8000)" != "200" ]]; do echo "waiting for Nautobot"; sleep 5; done' || false

    echo "# Populating Nautobot for running integration tests.."
    python ./tests/integration/nautobot-populate.py

    echo "# Running..."
    # shellcheck disable=SC2086
    ansible-test integration $ANSIBLE_INTEGRATION_ARGS --coverage --python "$PYTHON_VERSION" regression-latest "$@"
    ansible-test integration $ANSIBLE_INTEGRATION_ARGS --coverage --python "$PYTHON_VERSION" latest "$@"
    ansible-test coverage report
}

main "$@"
