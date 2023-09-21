#!/usr/bin/env bash

# Stop on failure - if unit tests fail the inventory will not be updated
set -e

# - Build Nautobot via development environment
# - Fill with test data, run ./tests/integration/nautobot-populate.py
# - Add '127.0.0.1 nautobot' to /etc/hosts
# - Run ./hacking/update_test_inventories.sh
# - Manually verify the diff of new JSON is correct, to prevent introducing a regression.

# Install locally
export ANSIBLE_COLLECTIONS_PATHS=.
export OUTPUT_INVENTORY_JSON=tests/integration/targets/inventory/files

# Remove local cache
rm -rf /tmp/inventory_nautobot/

# Clean and install the built collection
./hacking/build.sh

# Install new built version
ansible-galaxy collection install networktocode-nautobot-*.tar.gz -p .

# Run the same script used by integration tests, but save the results
./tests/integration/targets/inventory/runme.sh
