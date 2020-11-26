---
uuid: f319d6f6-bd45-4e18-b232-45b270fd1c29
---
# Network | OSPF | Neighbor Up

OSPF neighbor up

## Symptoms

Routing table changes

## Probable Causes

An OSPF adjacency was established with the indicated neighboring router. The local router can now exchange information with it.

## Recommended Actions

No specific actions needed

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
area | str | :material-check: | OSPF area
interface | interface_name | :material-close: | Interface
neighbor | ip_address | :material-close: | Neighbor's Router ID
reason | str | :material-check: | Adjacency lost reason
from_state | str | :material-check: | from state
to_state | str | :material-check: | to state
vrf | str | :material-check: | VRF

## Alarms

### Clearing alarms

`Network | OSPF | Neighbor Up` events may clear following alarms:

Alarm Class | Description
--- | ---
`Network | OSPF | Neighbor Down` | dispose
