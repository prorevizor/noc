---
uuid: f7a27faf-3b5d-45a6-b3f3-bedf20ea3337
---
# airflow Model Interface

Airflow direction for cooling. May be set for rack to show desired
airflow movement from *cold* to *hot* area, and for equipment to show
constructive air movement

## Variables

| Name | Type | Description | Required | Constant | Default |
| --- | --- | --- | --- | --- | --- |
| inlet   | String | Direction of cold inlet:  | No       | No       |         |
|         |        | * `f` - forward           |          |          |         |
|         |        | * `r` - rear              |          |          |         |
|         |        | * `b` - bottom            |          |          |         |
|         |        | * `t` - top               |          |          |         |
|         |        | * `l` - left              |          |          |         |
|         |        | * `r` - right             |          |          |         |
| exhaust | String | Direction of hot exhaust: | No       | No       |         |
|         |        | * `f` - forward           |          |          |         |
|         |        | * `r` - rear              |          |          |         |
|         |        | * `b` - bottom            |          |          |         |
|         |        | * `t` - top               |          |          |         |
|         |        | * `l` - left              |          |          |         |
|         |        | * `r` - right             |          |          |         |

## Examples
```json
{
  "airflow": {
    "exhaust": "l",
    "intake": "r"
  }
}
```
  
