# Migrating from `query_graphql`

The `query_graphql` module is deprecated as of v6.2.0 and will be removed in v7.0.0. It has been replaced by two focused modules that follow Ansible naming conventions:

- **`graphql_info`** — queries the GraphQL endpoint and returns data via `register`
- **`graphql_facts`** — queries the GraphQL endpoint and sets the returned data as Ansible facts

## Which module should I use?

| I want to...                                          | Use               |
|-------------------------------------------------------|-------------------|
| Query data and reference it later via a variable      | `graphql_info`    |
| Query data and make it available as host facts        | `graphql_facts`   |

## Migration guide

### `query_graphql` without `update_hostvars` → `graphql_info`

The default behavior of `query_graphql` (with `update_hostvars: false`) maps directly to `graphql_info`. Data is returned under the `data` key of the registered variable.

**Before:**

```yaml
- name: Obtain list of locations from Nautobot
  networktocode.nautobot.query_graphql:
    url: http://nautobot.local
    token: thisIsMyToken
    query: "{{ query_string }}"
  register: result

- name: Use the result
  debug:
    msg: "{{ result.data.locations }}"
```

**After:**

```yaml
- name: Obtain list of locations from Nautobot
  networktocode.nautobot.graphql_info:
    url: http://nautobot.local
    token: thisIsMyToken
    query: "{{ query_string }}"
  register: result

- name: Use the result
  debug:
    msg: "{{ result.data.locations }}"
```

### `query_graphql` with `update_hostvars: true` → `graphql_facts`

When `update_hostvars: true` was set, `query_graphql` would populate `ansible_facts` so that the query's root keys were accessible directly on the host. `graphql_facts` always does this — no option needed.

**Before:**

```yaml
- name: Obtain list of locations from Nautobot
  networktocode.nautobot.query_graphql:
    url: http://nautobot.local
    token: thisIsMyToken
    query: "{{ query_string }}"
    update_hostvars: true

- name: Use the result
  debug:
    msg: "{{ locations }}"
```

**After:**

```yaml
- name: Obtain list of locations from Nautobot
  networktocode.nautobot.graphql_facts:
    url: http://nautobot.local
    token: thisIsMyToken
    query: "{{ query_string }}"

- name: Use the result
  debug:
    msg: "{{ locations }}"
```

!!! note
    `graphql_facts` does not require `register` — the query's root keys are automatically added to `ansible_facts` and become available as host variables.

## Key differences summary

| Feature                        | `query_graphql`            | `graphql_info`  | `graphql_facts`  |
|-------------------------------|----------------------------|-----------------|------------------|
| Returns `data` key            | Always                     | Always          | Always           |
| Sets `ansible_facts`          | Only with `update_hostvars: true` | Never  | Always           |
| `update_hostvars` parameter   | Yes                        | No              | No               |
| Requires `register`           | To access `data`           | Yes             | No               |
| Deprecated                    | Yes (removed in v7.0.0)    | No              | No               |
