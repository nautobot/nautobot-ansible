# Testing with GitHub Actions

## Overview

The GitHub Actions workflows are designed to test the collection in a CI/CD environment.

## Linting, Unit Testing, and Integration Testing

After you have commit your code and published your branch, you can run the manual tests by going to the [Actions](https://github.com/networktocode/nautobot-ansible/actions) page and selecting the `Manual Tests` workflow. Next, click on the `Run workflow` button and select your branch. If you would like to run the full integration tests, you can enable the `Run full integration tests` option. This option will run the tests against all supported versions of Nautobot and Ansible, so it takes a bit longer to run.

## Galaxy Importer Test

The Galaxy Importer workflow tests the collection with the [Galaxy Importer](https://github.com/ansible/galaxy-importer) library, which is the same tool Red Hat's automation-hub runs when a release is published. It runs automatically as the `galaxy_importer` job on every pull request, and can also be run on demand by going to the [Actions](https://github.com/networktocode/nautobot-ansible/actions) page, selecting the `Galaxy Importer Manual Test` workflow, clicking `Run workflow`, and selecting your branch.

### Which versions the job runs against

The job installs `ansible-core` at the **oldest version this collection claims to support** and leaves `ansible-lint` unpinned.

The `ansible-core` version is derived at runtime from the `requires_ansible` floor in `meta/runtime.yml`, not hardcoded in the workflow. That keeps a single source of truth: raising the floor needs no change to the workflow, and the two can never drift. It also avoids a trap — pinning *below* the declared floor makes the `ansible-doc` sanity test fail on `collection does not support Ansible version X.Y`, which would leave the job permanently red for a reason unrelated to any real publish blocker.

`ansible-lint` is deliberately **not** pinned. galaxy-importer constrains the version itself, and automation-hub tracks whatever galaxy-importer ships, so installing the same unpinned set is closer to the real publish gate than any version we could guess from an import log.

This makes the check answer a question worth asking — *does the collection still import cleanly at our declared floor, under the importer's own lint profile?* — rather than trying to replicate a Red Hat toolchain we cannot observe. `invoke lint` and the `unit` job cover the newer end of the supported range; this job covers the oldest end plus the build-and-import round trip that nothing else exercises.

### How failures are reported

!!! warning

    The Galaxy Importer library is not designed to fail (exit with a non-zero exit code) when it encounters linting or testing errors, and it runs `ansible-test sanity` with `--failure-ok` internally. The workflow therefore inspects the importer log itself and fails the job on any finding, rather than relying on the importer's exit code.

The job fails on both of the log levels that carry real findings:

- `ERROR:` — fatal import errors, plus the `ansible-test sanity` output the importer echoes through. This is the level [#740](https://github.com/nautobot/nautobot-ansible/issues/740) surfaced at.
- `WARNING:` — `ansible-lint` rule violations. This is the level [#739](https://github.com/nautobot/nautobot-ansible/issues/739) surfaced at, so warnings cannot be ignored. Matching only `ERROR:` would sail straight past the #739 class of finding.

The gate strips ANSI color escapes from the log before matching. galaxy-importer invokes `ansible-test sanity` with `--color yes`, so the `ERROR:` lines it echoes through are wrapped in escape sequences and do not literally start with `ERROR:`. This is also why the upstream community action's `line.startswith('ERROR:')` check never even annotated #740.

Because `WARNING:` is treated as a failure, the workflow keeps a small allowlist of importer output that does not block publication. Today that allowlist holds one entry: galaxy-importer's own notice that `tests/sanity/ignore-*.txt` exists. That check scans `tests/sanity/` regardless of the pinned core version, so the notice fires on every run as long as the repository ships any ignore file. If you add to the allowlist, keep it as narrow as possible and comment why the entry is safe — an over-broad allowlist turns this job back into the decorative check it used to be.
