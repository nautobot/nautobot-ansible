# Module code generator

Generates `plugins/modules/` from the Nautobot REST API. See
[docs/getting_started/contributing/modules/code_generator.md](../../docs/getting_started/contributing/modules/code_generator.md).

```bash
invoke start
invoke codegen          # update the module configs and modules
invoke codegen --check  # what CI runs: fail if anything would change
invoke codegen-tests
```
