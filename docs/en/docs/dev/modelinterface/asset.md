---
e8e9a35f-d051-4b11-8e0b-0d14dcbdffb1
---

# asset Model Interface

Inventory references, asset and serial numbers

## Variables

| Name            | Type        | Description                               | Required         | Constant         | Default |
| --------------- | ----------- | ----------------------------------------- | ---------------- | ---------------- |---------|
| part_no         | String List | Internal vendor's part number             | :material-check: | :material-check: |         |
|                 |             | as shown by diagnostic commands           |                  |                  |         |
| order_part_no   | String List | Vendor's [FRU](../../glossary.md#fru) as shown | :material-close: | :material-check: |         |
|                 |             | in catalogues and price lists             |                  |                  |         |
| serial          | String      | Item's serial number                      | :material-close: |                  |         |
| revision        | String      | Item's hardware revision                  | :material-close: |                  |         |
| asset_no        | String      | Item's asset number, used for             | :material-close: |                  |         |
|                 |             | asset tracking in accounting              |                  |                  |         |
|                 |             | system                                    |                  |                  |         |
| mfg_date        | String      | Manufacturing date in                     | :material-close: |                  |         |
|                 |             | YYYY-MM-DD format                         |                  |                  |         |
| cpe_22          | String      | CPE v2.2 identification string            | :material-close: | :material-check: |         |
| cpe_23          | String      | CPE v2.3 identification string            | :material-close: | :material-check: |         |
| min_serial_size | Integer     | Minimal valid serial number size          | :material-close: | :material-check: |         |
| max_serial_size | Integer     | Maximal valid serial number size          | :material-close: | :material-check: |         |
| serial_mask     | String      | Regular expression to check serial number | :material-close: | :material-check: |         |

## Examples

```json
{
  "asset": {
    "order_part_no": ["MX-MPC2E-3D-Q"],
    "part_no": ["750-038493"]
  }
}
```
