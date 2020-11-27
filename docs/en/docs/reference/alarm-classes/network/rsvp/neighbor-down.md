---
uuid: a1086b80-e78b-4efe-b462-2ee0f2808a85
---
# Network | RSVP | Neighbor Down

## Symptoms

Routing table changes and possible lost of connectivity

## Probable Causes

Link failure or protocol misconfiguration

## Recommended Actions

Check links and local and neighbor router configuration

## Variables

Variable | Description | Default
--- | --- | ---
interface | Interface | `:material-close:`
neighbor | Neighbor's NSAP or name | `:material-close:`
reason | Neighbor lost reason | `:material-close:`

## Events

### Opening Events
`Network | RSVP | Neighbor Down` may be raised by events

Event Class | Description
--- | ---
`Network | RSVP | Neighbor Down` | dispose

### Closing Events
`Network | RSVP | Neighbor Down` may be cleared by events

Event Class | Description
--- | ---
`Network | RSVP | Neighbor Up` | dispose
