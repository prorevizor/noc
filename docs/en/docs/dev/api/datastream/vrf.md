# vrf DataStream

*vrf* DataStream contains summarized IPAM VRF state

## Fields


| Name            | Type            | Description                                        |
|-----------------|-----------------|----------------------------------------------------|
| id              | String          | VRF id                                             |
| change_id       | String          | :ref:`Record's change id<api-datastream-changeid>` |
| name            | String          | VRF name                                           |
| vpn_id          | String          | VPN ID                                             |
| afi             | Object          | Enabled Address Families                           |
| * ipv4          | Boolean         | IPv4 is enabled on VRF                             |
| * ipv6          | Boolean         | IPv6 is enabled on VRF                             |
| description     | String          | VRF textual description                            |
| rd              | String          | VRF route distinguisher                            |
| tags            | Array of String | VRF tags                                           |
| state           | Object          | VRF workflow state                                 |
|* id             | String          | State id                                           |
|* name           | String          | State name                                         |
|* workflow       | Object          | VRF workflow                                       |
|** id            | String          | Workflow id                                        |
|** name          | String          | Workflow name                                      |
|* allocated_till | Datetime        | Workflow state deadline                            |
| profile         | Object          | VRF Profile                                        |
|* id             | String          | VRF Profile id                                     |
|* name           | String          | VRF Profile name                                   |
| project         | Object          | VRF Project                                        |
|* id             | String          | Project id                                         |
|* name           | String          | Project name                                       |
| source          | String          | VRF Learning source:                               |
|                 |                 |  * `M` - Manual                                     |
|                 |                 |  * `i` - Interface                                  |
|                 |                 |  * `m` - MPLS                                       |
|                 |                 |  * `c` - ConfDB                                     |


## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:vrf` permissions
required.
