---
uuid: bd8fa1b4-9bd9-4bef-a557-756255ccad1e
---
# Network | PIM | DR Change

## Symptoms

Some multicast flows lost

## Probable Causes

Link failure or protocol misconfiguration

## Recommended Actions

Check links and local and neighbor router configuration

## Variables

Variable | Description | Default
--- | --- | ---
interface | Interface | `:material-close:`
from_dr | From DR | `:material-close:`
to_dr | To DR | `:material-close:`
vrf | VRF | `:material-close:`

## Events

### Opening Events
`Network | PIM | DR Change` may be raised by events

Event Class | Description
--- | ---
`Network | PIM | DR Change` | dispose
