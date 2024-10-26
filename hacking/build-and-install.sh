#!/usr/bin/env bash

# Usage: ./hacking/build.sh

# Remove previous test installs
rm -r ansible_collections 2>/dev/null || true

# Remove old built versions
rm networktocode-nautobot-*.tar.gz 2>/dev/null || true

# Remove test output
rm -r tests/output 2>/dev/null || true
rm -r .pytest_cache 2>/dev/null || true

# Build the collection
ansible-galaxy collection build --force --verbose .

# Extract version from pyproject.toml, remove quotes and spaces
VERSION=$(grep '^version' ./pyproject.toml | awk -F= '{print $2}' | tr -d ' "')

echo "Extracted version: ${VERSION}"

# Form the collection filename correctly and install it
TAR_FILE="networktocode-nautobot-${VERSION}.tar.gz"
echo "${TAR_FILE}"

ansible-galaxy collection install "${TAR_FILE}" --force
