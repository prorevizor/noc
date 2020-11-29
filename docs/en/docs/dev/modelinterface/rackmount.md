---
b26d8388-0450-4c30-886d-d3d6da86c401
---

# rackmount Model Interface

Rack mounted equipment.
Used to store position in rack.


## Variables

| Name     | Type   | Description                                      | Required         | Constant         | Default   |
| -------- | ------ | ------------------------------------------------ | ---------------- | ---------------- | --------- |
| units    | float  | Size in units                                    | :material-check: | :material-check: |           |
| position | int    | Bottom rack position (in units)                  | :material-close: | :material-close: |           |
| side     | str    | Mounting side (f/r)                              | :material-close: | :material-close: |           |
|          |        |                                                  |                  |                  |           |
|          |        | f - mounted at the front side                    |                  |                  |           |
|          |        | r - mounted at the rear side                     |                  |                  |           |
| shift    | int    | Shift 0/1/2 holes up                             | :material-close: | :material-close: |           |
|          |        |                                                  |                  |                  |           |
|          |        | 0 - fit to the unit                              |                  |                  |           |
|          |        | 1 - displacement 1 hole up relative to the unit  |                  |                  |           |
|          |        | 2 - displacement 2 holes up relative to the unit |                  |                  |           |

## Examples

```json
{
  "rackmount": {
     "units": 1.0
  }
}
```
