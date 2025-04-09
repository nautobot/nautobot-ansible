# Testing with GitHub Actions

## Overview

The GitHub Actions workflows are designed to test the collection in a CI/CD environment.

## Linting, Unit Testing, and Integration Testing

After you have commit your code and published your branch, you can run the manual tests by going to the [Actions](https://github.com/networktocode/nautobot-ansible/actions) page and selecting the `Manual Tests` workflow. Next, click on the `Run workflow` button and select your branch. If you would like to run the full integration tests, you can enable the `Run full integration tests` option. This option will run the tests against all supported versions of Nautobot and Ansible, so it takes a bit longer to run.

## Galaxy Importer Test

The Galaxy Importer Manual Test workflow is designed to test the collection with the [Galaxy Importer](https://github.com/ansible/galaxy-importer) library. You can run this workflow manually by going to the [Actions](https://github.com/networktocode/nautobot-ansible/actions) page and selecting the `Galaxy Importer Manual Test` workflow. Next, click on the `Run workflow` button and select your branch.

!!! warning

    The Galaxy Importer library is not designed to fail (exit with a non-zero exit code) if it encounters any linting or testing errors so the CI will not fail either. You will need to check the logs to determine if there are any issues that need to be addressed.
