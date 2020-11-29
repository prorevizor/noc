---
c3cb0577-9ed2-4edb-b3e3-eaca6f1fed38
---

# stack Model Interface

Indication of stack/virtual chassis/cluster

## Variables

| Name      | Type   | Description           | Required         | Conastant        | Default   |
| --------- | ------ | --------------------- | ---------------- | ---------------- | --------- |
| stackable | bool   | Object can be stacked | :material-close: | :material-check: |           |
| member    | str    | Stack member id       | :material-close: | :material-close: |           |

## Examples

```json
{
  "stack": {
    "stackable": true
  }
}
```
