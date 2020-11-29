# address DataStream

`address` [DataStream](index.md) contains summarized IPAM Address state

## Fields

| Name                                               | Type                         | Description                              |
| -------------------------------------------------- | ---------------------------- | ---------------------------------------- |
| id                                                 | String                       | Address id                               |
| change_id                                          | String                       | [Record's Change Id](index.md#change-id) |
| name                                               | String                       | Address name                             |
| address                                            | String                       | Address (i.e. `192.168.0.1`)             |
| fqdn                                               | String                       | Fully-Qualified Domain Name for address  |
| afi                                                | String                       | Address family:                          |
|                                                    |                              | \* `ipv4`                                |
|                                                    |                              | \* `ipv6`                                |
| description                                        | String                       | Address textual description              |
| mac                                                | String                       | Related MAC address                      |
| subinterface                                       | String                       | Related subinterface name                |
| tags                                               | Array of String              | VRF tags                                 |
| state                                              | Object :material-arrow-down: | VRF workflow state                       |
| :material-arrow-right: id                          | String                       | State id                                 |
| :material-arrow-right: name                        | String                       | State name                               |
| :material-arrow-right: workflow                    | Object :material-arrow-down: | VRF workflow                             |
| :material-arrow-right: :material-arrow-right: id   | String                       | Workflow id                              |
| :material-arrow-right: :material-arrow-right: name | String                       | Workflow name                            |
| :material-arrow-right: allocated_till              | Datetime                     | Workflow state deadline                  |
| profile                                            | Object :material-arrow-down: | Address Profile                          |
| :material-arrow-right: id                          | String                       | Address Profile id                       |
| :material-arrow-right: name                        | String                       | Address Profile name                     |
| vrf                                                | Object :material-arrow-down: | Prefix VRF                               |
| :material-arrow-right: id                          | String                       | VRF id                                   |
| :material-arrow-right: name                        | String                       | VRF name                                 |
| project                                            | Object :material-arrow-down: | Address Project                          |
| :material-arrow-right: id                          | String                       | Project id                               |
| :material-arrow-right: name                        | String                       | Project name                             |
| source                                             | String                       | VRF Learning source:                     |
|                                                    |                              | \* `M` - Manual                          |
|                                                    |                              | \* `i` - Interface                       |
|                                                    |                              | \* `m` - Management                      |
|                                                    |                              | \* `d` - DHCP                            |
|                                                    |                              | \* `n` - Neighbor                        |

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:address` permission
is required.
