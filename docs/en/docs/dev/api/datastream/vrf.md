# vrf DataStream

`vrf` [DataStream](index.md) contains summarized IPAM VRF state

## Fields

| Name                                               | Type                         | Description                              |
| -------------------------------------------------- | ---------------------------- | ---------------------------------------- |
| id                                                 | String                       | VRF id                                   |
| change_id                                          | String                       | [Record's Change Id](index.md#change-id) |
| name                                               | String                       | VRF name                                 |
| vpn_id                                             | String                       | VPN ID                                   |
| afi                                                | Object :material-arrow-down: | Enabled Address Families                 |
| :material-arrow-right: ipv4                        | Boolean                      | IPv4 is enabled on VRF                   |
| :material-arrow-right: ipv6                        | Boolean                      | IPv6 is enabled on VRF                   |
| description                                        | String                       | VRF textual description                  |
| rd                                                 | String                       | VRF route distinguisher                  |
| tags                                               | Array of String              | VRF tags                                 |
| state                                              | Object :material-arrow-down: | VRF workflow state                       |
| :material-arrow-right: id                          | String                       | State id                                 |
| :material-arrow-right: name                        | String                       | State name                               |
| :material-arrow-right: workflow                    | Object :material-arrow-down: | VRF workflow                             |
| :material-arrow-right: :material-arrow-right: id   | String                       | Workflow id                              |
| :material-arrow-right: :material-arrow-right: name | String                       | Workflow name                            |
| :material-arrow-right: allocated_till              | Datetime                     | Workflow state deadline                  |
| profile                                            | Object :material-arrow-down: | VRF Profile                              |
| :material-arrow-right: id                          | String                       | VRF Profile id                           |
| :material-arrow-right: name                        | String                       | VRF Profile name                         |
| project                                            | Object :material-arrow-down: | VRF Project                              |
| :material-arrow-right: id                          | String                       | Project id                               |
| :material-arrow-right: name                        | String                       | Project name                             |
| source                                             | String                       | VRF Learning source:                     |
|                                                    |                              | \* `M` - Manual                          |
|                                                    |                              | \* `i` - Interface                       |
|                                                    |                              | \* `m` - MPLS                            |
|                                                    |                              | \* `c` - ConfDB                          |

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:vrf` permissions
required.
