---
uuid: 8f8892fe-cc85-4c4f-b8e9-4a0a168e6149
---
# Network | PIM | DR Change

Designated Router Change

## Symptoms

Some multicast flows lost

## Probable Causes

PIM protocol configuration problem or link failure

## Recommended Actions

Check links and local and neighbor's router configuration

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
interface | interface_name | :material-close: | Interface
from_dr | ip_address | :material-close: | From DR
to_dr | ip_address | :material-close: | To DR
vrf | str | :material-check: | VRF

## Alarms

### Raising alarms

`Network | PIM | DR Change` events may raise following alarms:

Alarm Class | Description
--- | ---
`Network | PIM | DR Change` | dispose
