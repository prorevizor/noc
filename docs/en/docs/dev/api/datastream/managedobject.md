# managedobject DataStream

`managedobject` [DataStream](index.md) contains summarized :ref:`Managed Object<reference-managed-object>`
state, including capabilities, interfaces and topology

## Fields

| Name                                                                     | Type                                  | Description                                                            |
| ------------------------------------------------------------------------ | ------------------------------------- | ---------------------------------------------------------------------- |
| id                                                                       | String                                | :ref:`Managed Object's<reference-managed-object>` id                   |
| change_id                                                                | String                                | [Record's Change Id](index.md#change-id)                               |
| remote_system                                                            | Object :material-arrow-down:          | Source :ref:`remote system<reference-remote-system>` for object        |
| :material-arrow-right: id                                                | String                                | External system's id                                                   |
| :material-arrow-right: name                                              | String                                | External system's name                                                 |
| remote_id                                                                | String                                | External system's id (Opaque attribbute)                               |
| bi_id                                                                    | Integer                               | BI Database id (metrics)                                               |
| name                                                                     | String                                | Object's name                                                          |
| profile                                                                  | String                                | :ref:`SA Profile<profiles>`                                            |
| vendor                                                                   | String                                | Vendor                                                                 |
| platform                                                                 | String                                | Platform                                                               |
| version                                                                  | String                                | Firmware version                                                       |
| address                                                                  | String                                | Management Address                                                     |
| description                                                              | String                                | Managed Object description                                             |
| tags                                                                     | Array of String                       | Managed Object tags                                                    |
| is_managed                                                               | Boolean                               | Object is managed                                                      |
| object_profile                                                           | Object :material-arrow-down:          | :ref:`Managed Object Profile's data<reference-managed-object-profile>` |
| :material-arrow-right: id                                                | String                                | Profile's ID                                                           |
| :material-arrow-right: name                                              | String                                | Profile's Name                                                         |
| :material-arrow-right: level                                             | Integer                               | Managed Object's :ref:`level<reference-managed-object-profile-level>`  |
| :material-arrow-right: enable_ping                                       | Boolean                               | Ping probe is enabled                                                  |
| :material-arrow-right: enable_box                                        | Boolean                               | :ref:`Box discovery<discovery-box>` is enabled                         |
| :material-arrow-right: enable_periodic                                   | Boolean                               | :ref:`Periodic discovery<discovery-periodic>` is enabled               |
| :material-arrow-right: tags                                              | Array of String                       | Managed Object Profile tags                                            |
| config                                                                   | Object :material-arrow-down:          | Optional Object's config metadata (if any)                             |
| :material-arrow-right: revision                                          | String                                | Config revision ID                                                     |
| :material-arrow-right: size                                              | Integer                               | Config size in octets                                                  |
| :material-arrow-right: updated                                           | String                                | Last modification timestamp in ISO 8601 format                         |
| capabilities                                                             | Array of Object :material-arrow-down: | List of object's :ref:`capabilities<caps>`                             |
| :material-arrow-right: name                                              | String                                | Capability's name                                                      |
| :material-arrow-right: value                                             | String                                | Capabbility's value                                                    |
| service_groups                                                           | Array of Object :material-arrow-down: | Service :ref:`Resource Groups<reference-resource-group>`               |
| :material-arrow-right: id                                                | String                                | :ref:`Resource Group's<reference-resource-group>` id                   |
| :material-arrow-right: name                                              | String                                | :ref:`Resource Group's<reference-resource-group>` id                   |
| :material-arrow-right: technology                                        | String                                | :ref:`Technology's<reference-technology>` name                         |
| :material-arrow-right: static                                            | Boolean                               | true if group is static                                                |
| client_groups                                                            | Array of Object :material-arrow-down: | Client :ref:`Resource Groups<reference-resource-group>`                |
| :material-arrow-right: id                                                | String                                | :ref:`Resource Group's<reference-resource-group>` id                   |
| :material-arrow-right: name                                              | String                                | :ref:`Resource Group's<reference-resource-group>` id                   |
| :material-arrow-right: technology                                        | String                                | :ref:`Technology's<reference-technology>` name                         |
| :material-arrow-right: static                                            | Boolean                               | true if group is static                                                |
| forwarding-instances                                                     | Array of Object :material-arrow-down: | List of VPNs and virtual tables                                        |
| :material-arrow-right: name                                              | String                                | Forwarding instance name                                               |
| :material-arrow-right: type                                              | String                                | Forwarding instance type. One of:                                      |
|                                                                          |                                       | table, bridge, vrf, vll, vpls, evpn, vxlan                             |
| :material-arrow-right: rd                                                | String                                | VPN route-distinguisher                                                |
| :material-arrow-right: vpn_id                                            | String                                | Globally-unique VPN id                                                 |
| :material-arrow-right: rt_export                                         | Array of String                       | List of exported route-targets                                         |
| :material-arrow-right: rt_import                                         | Array of String                       | List of imported route-targets                                         |
| :material-arrow-right: subinterfaces                                     | Array of String                       | List of subinterfaces in given forwarding instance                     |
| interfaces                                                               | Array of Object :material-arrow-down: | List of physical interfaces                                            |
| :material-arrow-right: name                                              | String                                | Interface's name (Normalized by profile)                               |
| :material-arrow-right: type                                              | String                                | Interface's type                                                       |
| :material-arrow-right: admin_status                                      | Boolean                               | Administrative status of interface                                     |
| :material-arrow-right: enabled_protocols                                 | Array of String                       | List of active protocols                                               |
| :material-arrow-right: description                                       | String                                | Description                                                            |
| :material-arrow-right: hints                                             | Array of String                       | List of optional hints, like `uni`, `nni`                              |
| :material-arrow-right: snmp_ifindex                                      | Integer                               | SNMP ifIndex                                                           |
| :material-arrow-right: mac                                               | String                                | MAC-address                                                            |
| :material-arrow-right: aggregated_interface                              | String                                | LAG interfacename (for LAG members)                                    |
| :material-arrow-right: subinterfaces                                     | Array of Object :material-arrow-down: | List of logical interfaces                                             |
| :material-arrow-right: :material-arrow-right: name                       | String                                | Subinterface name (Normalized by profile)                              |
| :material-arrow-right: :material-arrow-right: description                | String                                | Description                                                            |
| :material-arrow-right: :material-arrow-right: mac                        | String                                | MAC-address                                                            |
| :material-arrow-right: :material-arrow-right: enabled_afi                | Array of String                       | Active address families                                                |
| :material-arrow-right: :material-arrow-right: ipv4_addresses             | Array of String                       | List of IPv4 addresses                                                 |
| :material-arrow-right: :material-arrow-right: ipv6_addresses             | Array of String                       | List of IPv6 addresses                                                 |
| :material-arrow-right: :material-arrow-right: iso_addresses              | Array of String                       | List of ISO/CLNS addresses                                             |
| :material-arrow-right: :material-arrow-right: vpi                        | Integer                               | ATM VPI                                                                |
| :material-arrow-right: :material-arrow-right: vci                        | Integer                               | ATM VCI                                                                |
| :material-arrow-right: :material-arrow-right: enabled_protocols          | Array of String                       | Enabled protocols                                                      |
| :material-arrow-right: :material-arrow-right: snmp_ifindex               | Integer                               | SNMP ifIndex                                                           |
| :material-arrow-right: :material-arrow-right: untagged_vlan              | Integer                               | Untagged VLAN (for BRIDGE)                                             |
| :material-arrow-right: :material-arrow-right: tagged_vlan                | Array of Integer                      | List of tagged VLANs (for BRIDGE)                                      |
| :material-arrow-right: :material-arrow-right: vlan_ids                   | Array of Integer                      | Stack of VLANs for L3 interfaces                                       |
| :material-arrow-right: link                                              | Array of Object :material-arrow-down: | List of links                                                          |
| :material-arrow-right: :material-arrow-right: object                     | Integer                               | Remote object\'s ID                                                    |
| :material-arrow-right: :material-arrow-right: interface                  | String                                | Remote port's name (interfaces.name)                                   |
| :material-arrow-right: :material-arrow-right: method                     | String                                | Discovery method                                                       |
| :material-arrow-right: :material-arrow-right: is_uplink                  | Boolean                               | True, if link is uplink                                                |
| :material-arrow-right: services                                          | Array of Object :material-arrow-down: | Services related to the port                                           |
| :material-arrow-right: :material-arrow-right: id                         | String                                | Service\'s ID                                                          |
| :material-arrow-right: :material-arrow-right: remote_system              | Object                                | Source :ref:`remote system<reference-remote-system>` for service       |
| :material-arrow-right: :material-arrow-right::material-arrow-right: id   | String                                | External system's id                                                   |
| :material-arrow-right: :material-arrow-right::material-arrow-right: name | String                                | External system's name                                                 |
| :material-arrow-right: :material-arrow-right: remote_id                  | String                                | Service id in External system (Opaque attribute)                       |
| asset                                                                    | Array of Object :material-arrow-down: | Hardware configuration/Inventory data                                  |
| :material-arrow-right: id                                                | String                                | Inventory object\'s ID                                                 |
| :material-arrow-right: model                                             | Object :material-arrow-down:          | Inventory model (Object model)                                         |
| :material-arrow-right: :material-arrow-right: id                         | String                                | Inventory model\'s ID                                                  |
| :material-arrow-right: :material-arrow-right: name                       | String                                | Inventory model\'s name                                                |
| :material-arrow-right: :material-arrow-right: tags                       | Array of String                       | :ref:`Object model's tags<dev-objectmodel-tags>`                       |
| :material-arrow-right: :material-arrow-right: vendor                     | Object :material-arrow-down:          | Inventory model\'s vendor                                              |
| :material-arrow-right: :material-arrow-right::material-arrow-right: id   | String                                | Vendor\'s ID                                                           |
| :material-arrow-right: :material-arrow-right::material-arrow-right: name | String                                | Vendor\'s Name                                                         |
| :material-arrow-right: serial                                            | String                                | Inventory object's serial number                                       |
| :material-arrow-right: revision                                          | String                                | Inventory object's hardware revision                                   |
| :material-arrow-right: data                                              | Object :material-arrow-down:          | Attached data (see :ref:`Model Interfaces<dev-modelinterface>`)        |
| :material-arrow-right: slots                                             | Array of Object :material-arrow-down: | Object's slots configuration                                           |
| :material-arrow-right: :material-arrow-right: name                       | String                                | Name of slot                                                           |
| :material-arrow-right: :material-arrow-right: direction                  | String                                | Slot's direction:                                                      |
|                                                                          |                                       |                                                                        |
|                                                                          |                                       | \* i - inner (nested object)                                           |
|                                                                          |                                       | \* s - same level (horizontal connection)                              |
| :material-arrow-right: :material-arrow-right: protocols                  | Array of String                       | List of protocols, supported by slot                                   |
|                                                                          |                                       | (see :ref:`Inventory Protocols <dev-inventory-protocols>`)             |
| :material-arrow-right: :material-arrow-right: interface                  | String                                | Optional interface name related to the slot                            |
| :material-arrow-right: :material-arrow-right: slots                      | Array of Object :material-arrow-down: | List of inner slots for `i` direction, same structure as `slots`       |

## Filters

### pool(name)

Restrict stream to objects belonging to pool `name`

name
: Pool name

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:managedobject` permissions
required.
