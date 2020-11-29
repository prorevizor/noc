---
b20b514d-954b-4fcc-b783-19328277c289
---

# sector Model Interface

Antenna sector, it is usually used in a combination about a [ModelInterface Geopoint](geopoint.md).

## Variables

| Name        | Type   | Description                      | Required         | Constant         | Default   |
| ----------- | ------ | -------------------------------- | ---------------- | ---------------- | --------- |
| bearing     | float  | Bearing angle                    | :material-check: | :material-close: |           |
| elevation   | float  | Elevation angle                  | :material-check: | :material-close: | 0         |
| height      | float  | Height above ground (in meters)  | :material-check: | :material-close: | 0         |
| h_beamwidth | float  | Horizontal beamwidth (in angles) | :material-check: | :material-check: |           |
| v_beamwidth | float  | Vertical beamwidth (in angles)   | :material-check: | :material-check: |           |
