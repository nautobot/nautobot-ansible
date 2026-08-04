# CLAUDE.md - AI Development Guide for nautobot-ansible

## Project Overview

This is the official Ansible Collection for Nautobot (network automation source of truth). Modules follow a DRY pattern using shared infrastructure in `plugins/module_utils/`.

## Architecture Pattern

All standard CRUD modules inherit from base classes in `module_utils/`:

```
plugins/
├── modules/           # Individual Ansible modules (thin wrappers)
│   ├── device.py     # ~150 lines, uses NautobotDcimModule
│   ├── tag.py        # ~150 lines, uses NautobotExtrasModule
│   └── ...
└── module_utils/     # Shared infrastructure
    ├── utils.py      # NautobotModule base class, arg specs, mappings
    ├── extras.py     # NautobotExtrasModule for extras/* endpoints
    ├── dcim.py       # NautobotDcimModule for dcim/* endpoints
    └── ...           # One file per Nautobot app
```

## Adding a New Standard Module

1. **Register endpoint** in `utils.py`:
   - Add to `API_APPS_ENDPOINTS` dict (maps endpoint to app)
   - Add to `ENDPOINT_NAME_MAPPING` (plural → singular)
   - Add to `ALLOWED_QUERY_PARAMS` (unique key combinations)
   - Add to `QUERY_TYPES` if lookup differs from "name"
   - Add to `CONVERT_TO_ID` if referenced by other modules

2. **Define endpoint constant** in the appropriate `module_utils/*.py`:
   ```python
   NB_MY_ENDPOINT = "my_endpoints"
   ```

3. **Create thin module** in `plugins/modules/`:
   ```python
   from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
       NB_MY_ENDPOINT,
       NautobotExtrasModule,
   )
   from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
       NAUTOBOT_ARG_SPEC,
       ID_ARG_SPEC,
   )
   
   def main():
       argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
       argument_spec.update(deepcopy(ID_ARG_SPEC))
       argument_spec.update(dict(
           # Module-specific args only
           name=dict(required=False, type="str"),
       ))
       module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
       my_module = NautobotExtrasModule(module, NB_MY_ENDPOINT)
       my_module.run()
   ```

## Non-Standard Endpoints (like scheduled_job)

Some modules have unusual API patterns (different create/read endpoints, no update support, etc.). These still MUST use shared utilities:

**Always import from utils.py:**
- `NAUTOBOT_ARG_SPEC` - base connection args
- `ID_ARG_SPEC` - standard id parameter
- `NautobotModule.is_valid_uuid()` - UUID validation

**Pattern for non-standard modules:**
```python
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    ID_ARG_SPEC,
    NautobotModule,
)

class NautobotScheduledJobModule(NautobotModule):
    """Custom module for non-standard scheduled_jobs endpoint."""
    
    def run(self):
        # Custom CRUD logic here
        pass
```

## Key Files

| File | Purpose |
|------|---------|
| `plugins/module_utils/utils.py` | Base class, shared arg specs, all endpoint mappings |
| `plugins/module_utils/extras.py` | `NautobotExtrasModule` for extras app |
| `plugins/module_utils/dcim.py` | `NautobotDcimModule` for dcim app |
| `plugins/modules/*.py` | Thin wrappers (~100-200 lines each) |

## Anti-Patterns to Avoid

❌ **Don't redefine `NAUTOBOT_ARG_SPEC`** - import it  
❌ **Don't reimplement `is_valid_uuid()`** - use `NautobotModule.is_valid_uuid()`  
❌ **Don't handle pynautobot connection manually** - use `NautobotModule.__init__`  
❌ **Don't write 400+ line modules** - if it's that big, refactor to use shared code  

## Testing

Integration tests live in `tests/integration/targets/latest/tasks/`.
Run with: `ansible-test integration --docker`

## Documentation Fragments

Reusable doc fragments in `plugins/doc_fragments/`:
- `fragments/base.py` - url, token, state, validate_certs
- `fragments/id.py` - id parameter
- `fragments/tags.py` - tags parameter
- `fragments/custom_fields.py` - custom_fields parameter

Use `extends_documentation_fragment` in module DOCUMENTATION.
