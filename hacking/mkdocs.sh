#!/usr/bin/env bash

# Create the docs_spec.json file from ansible-doc
ansible-doc --metadata-dump --no-fail-on-errors networktocode.nautobot >> docs/docs_spec.json