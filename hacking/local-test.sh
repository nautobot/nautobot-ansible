#!/usr/bin/env bash

################################################################################
# DEPRECATED
# Run `invoke unit` or `invoke integration` to run the tests locally instead!
################################################################################

# # Usage: ./hacking/local-test.sh

# # Run build, which will remove previously installed versions
# ./hacking/build.sh

# # Install new built version
# ansible-galaxy collection install networktocode-nautobot-*.tar.gz -p .

# # You can now cd into the installed version and run tests
# (cd ansible_collections/networktocode/nautobot/ && ansible-test units -v --python 3.9 && ansible-test sanity --requirements -v --python 3.9 --skip-test pep8 plugins/)
# rm -rf ansible_collections
