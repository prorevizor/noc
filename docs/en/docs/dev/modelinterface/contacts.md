---
91a24e0e-7d19-49f8-b127-c8a1bfa1c853
---

# contacts Model Interface

Administrative, billing and technical contacts for container
(PoP, Room, Rack)

## Variables

| Name             | Type    | Description                   | Required         |  Constant        | Default |
| ---------------- | ------- | ----------------------------- | ---------------- | ---------------- | ------- |
| has_contacts     | Boolean | Object can hold               | :material-check: | :material-check: | true    |
|                  |         | contact information           |                  |                  |        |
| administrative   | String  | Administrative contacts       | :material-close: | :material-close: |         |
|                  |         | including access and passes   |                  |                  |         |
| billing          | String  | Billing contacts, including   | :material-close: | :material-close: |         |
|                  |         | agreement negotiations,       |                  |                  |         |
|                  |         | bills and payments            |                  |                  |         |
| technical        | String  | Technical contacts,           | :material-close: | :material-close: |         |
|                  |         | including on-site engineering |                  |                  |         |

## Examples

```json
{
  "contacts": {
    "has_contacts": "true"
  }
}
```
