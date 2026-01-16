#!/bin/bash -eu

#########################################
# Docker entrypoint for integration tests
#
# This probably is usable locally in a native setup, but it isn't recommended.
# You should manually configure `integration_config.yml` instead and then run
# your tests.

set -o pipefail

function render {
  template="$1"; shift
  content="$(cat "$template")"

  eval "echo \"$content\""
}

function main {
    echo
    echo "# Running integration tests..."
    echo

    echo "# Rendering integration configuration"
    render "./tests/integration/integration_config.tmpl.yml" > ./tests/integration/integration_config.yml
    echo "# Creating inventory test config"
    render "./tests/integration/targets/inventory/runme_config.template" > ./tests/integration/targets/inventory/runme_config

    echo "# Checking to make sure Nautobot server is reachable.."
    # shellcheck disable=SC2016
    timeout 600 bash -c 'while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' nautobot:8000/health/)" != "200" ]]; do echo "waiting for Nautobot"; sleep 5; done' || false

    echo "# Populating Nautobot for running integration tests.."
    python ./tests/integration/nautobot-populate.py

    echo "# Running..."
    if [ "${SKIP_INVENTORY_TESTS}" != "true" ]; then
        # shellcheck disable=SC2086
        ansible-test integration $ANSIBLE_INTEGRATION_ARGS --coverage --requirements --python "$PYTHON_VERSION" inventory "$@"
    else
        echo "# Skipping inventory tests"
    fi
    if [ "${SKIP_REGRESSION_TESTS}" != "true" ]; then
        # shellcheck disable=SC2086
        ansible-test integration $ANSIBLE_INTEGRATION_ARGS --coverage --requirements --python "$PYTHON_VERSION" regression-latest "$@"
    else
        echo "# Skipping regression tests"
    fi
    # shellcheck disable=SC2086
    ansible-test integration $ANSIBLE_INTEGRATION_ARGS --coverage --requirements --python "$PYTHON_VERSION" latest "$@"
    ansible-test coverage report --requirements
}

main "$@"
