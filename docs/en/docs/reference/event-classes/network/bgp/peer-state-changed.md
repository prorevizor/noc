---
uuid: b4ab69c1-15d3-4dd9-a6c8-aecb25c249b0
---
# Network | BGP | Peer State Changed

BGP Peer State Changed

## Symptoms

## Probable Causes

## Recommended Actions

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
peer | ip_address | :material-close: | Peer
vrf | str | :material-check: | VRF
as | int | :material-check: | Peer AS
from_state | str | :material-check: | Initial state
to_state | str | :material-check: | Final state

## Alarms

### Raising alarms

`Network | BGP | Peer State Changed` events may raise following alarms:

Alarm Class | Description
--- | ---
`Network | BGP | Peer Down` | raise

### Clearing alarms

`Network | BGP | Peer State Changed` events may clear following alarms:

Alarm Class | Description
--- | ---
`Network | BGP | Peer Down` | clear_peer_down
`Network | BGP | Prefix Limit Exceeded` | clear_maxprefix
