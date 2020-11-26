---
uuid: 81375929-f945-40ea-abf5-f0a2c15095d8
---
# Network | PIM | Neighbor Up

PIM Neighbor up

## Symptoms

Multicast flows send successfully

## Probable Causes

PIM successfully established connect with neighbor

## Recommended Actions

No reaction needed

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
interface | interface_name | :material-close: | Interface
neighbor | ip_address | :material-close: | Neighbor's IP
vrf | str | :material-check: | VRF

## Alarms

### Clearing alarms

`Network | PIM | Neighbor Up` events may clear following alarms:

Alarm Class | Description
--- | ---
`Network | PIM | Neighbor Down` | dispose
