---
18fccfab-16c0-498f-9f6c-ae034a361bcd
---

# geopoint Model Interface

Linking point coordinates

## Variables

| Name   | Type   | Description                                      | Required         | Constant         | Default                                                   |
| ------ | ------ | ------------------------------------------------ | ---------------- | ---------------- | --------------------------------------------------------- |
| layer  | str    | Map layer code                                   | :material-check: | :material-check: |                                                           |
| srid   | str    | Spatial reference system, `autority:code` or `LOCAL` | :material-check: | :material-close:      | [EPSG:4326](http://spatialreference.org/ref/epsg/4326/)   |
| zoom   | int    | Default zoom level (override layer's default)    | :material-close: | :material-close: |                                                           |
| x      | float  | x coordinate, in SRS units                       | :material-check: | :material-close: |                                                           |
| y      | float  | y coordinate, in SRS units                       | :material-check: | :material-close: |                                                           |
| z      | float  | Height above ellipsoid, in meters                | :material-close: | :material-close: |                                                           |
| angle  | float  | Rotation angle, in degrees                       | :material-close: | :material-close: | 0.0                                                       |

Examples of Spatial reference systems:

| srid                                                    | Description                |
| ------------------------------------------------------- | -------------------------- |
| [EPSG:4326](http://spatialreference.org/ref/epsg/4326/) | GPS                        |
| [SR-ORG:95](http://spatialreference.org/ref/sr-org/95/) | Google Maps/Microsoft Live |


## Examples

```json
{
  "geopoint": {
    "layer": "pop_regional"
  }
}
```
