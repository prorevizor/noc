# prefix DataStream

`prefix` [DataStream](index.md) contains summarized IPAM Prefix state

## Fields

| Name                                               | Type                         | Description                              |
| -------------------------------------------------- | ---------------------------- | ---------------------------------------- |
| id                                                 | String                       | Prefix id                                |
| change_id                                          | String                       | [Record's Change Id](index.md#change-id) |
| name                                               | String                       | Prefix name                              |
| prefix                                             | String                       | Prefix (i.e. `192.168.0.0/24`)           |
| vpn_id                                             | String                       | VPN ID                                   |
| afi                                                | String                       | Prefix address family:                   |
|                                                    |                              |                                          |
|                                                    |                              | \* `ipv4`                                |
|                                                    |                              | \* `ipv6`                                |
| description                                        | String                       | Prefix textual description               |
| tags                                               | Array of String              | Prefix tags                              |
| state                                              | Object :material-arrow-down: | Prefix workflow state                    |
| :material-arrow-right: id                          | String                       | State id                                 |
| :material-arrow-right: name                        | String                       | State name                               |
| :material-arrow-right: workflow                    | Object :material-arrow-down: | Prefix workflow                          |
| :material-arrow-right: :material-arrow-right: id   | String                       | Workflow id                              |
| :material-arrow-right: :material-arrow-right: name | String                       | Workflow name                            |
| :material-arrow-right: allocated_till              | Datetime                     | Workflow state deadline                  |
| profile                                            | Object :material-arrow-down: | Prefix Profile                           |
| :material-arrow-right: id                          | String                       | Prefix Profile id                        |
| :material-arrow-right: name                        | String                       | Prefix Profile name                      |
| project                                            | Object :material-arrow-down: | Prefix Project                           |
| :material-arrow-right: id                          | String                       | Project id                               |
| :material-arrow-right: name                        | String                       | Project name                             |
| vrf                                                | Object                       | Prefix VRF                               |
| :material-arrow-right: id                          | String                       | VRF id                                   |
| :material-arrow-right: name                        | String                       | VRF name                                 |
| asn                                                | Object :material-arrow-down: | Prefix Autonomous System (AS)            |
| :material-arrow-right: id                          | String                       | AS id                                    |
| :material-arrow-right: name                        | String                       | AS name                                  |
| :material-arrow-right: asn                         | String                       | AS number (like `AS65000`)               |
| source                                             | String                       | VRF Learning source:                     |
|                                                    |                              |                                          |
|                                                    |                              | \* `M` - Manual                          |
|                                                    |                              | \* `i` - Interface                       |
|                                                    |                              | \* `w` - Whois                           |
|                                                    |                              | \* `n` - Neighbor                        |

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:prefix` permissions
required.
