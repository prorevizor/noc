---
uuid: a148d17b-feab-42ba-86c5-f83edc494495
---
# Network | OSPF | Neighbor Down

OSPF adjacency down

## Symptoms

Routing table changes and possible lost of connectivity

## Probable Causes

Link failure or protocol misconfiguration

## Recommended Actions

Check links and local and neighbor router configuration

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

### Raising alarms

`Network | OSPF | Neighbor Down` events may raise following alarms:

Alarm Class | Description
--- | ---
`Network | OSPF | Neighbor Down` | dispose
