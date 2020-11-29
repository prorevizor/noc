---
22e46608-0ed9-4822-b80f-d833a7f05e35
---

# twinax Model Interface

Twinax transceiver (two transceivers connected by cable in the assembly).
Both transceivers have the same serial number and can be inserted in one or two managed object.

## Variables

| Name        | Type   | Description                                | Required         | Constant         | Default   |
| ----------- | ------ | ------------------------------------------ | ---------------- | ---------------- | --------- |
| twinax      | bool   | Object is the twinax transceiver           | :material-check: | :material-check: |           |
| alias       | str    | Virtual connection name for ConnectionRule | :material-check: | :material-check: |           |
| connection1 | str    | Connection name for first side of twinax   | :material-check: | :material-check: |           |
| connection2 | str    | Connection name for second side of twinax  | :material-check: | :material-check: |           |
