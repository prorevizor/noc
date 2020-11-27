---
uuid: 8a0ffe77-c3c0-4327-b52b-7b482e710aec
---
# Network | BGP | Prefix Limit Exceeded

## Symptoms

## Probable Causes

## Recommended Actions

## Variables

Variable | Description | Default
--- | --- | ---
peer | BGP Peer | `:material-close:`
vrf | VRF | `:material-close:`
as | BGP Peer AS | `:material-close:`

## Events

### Opening Events
`Network | BGP | Prefix Limit Exceeded` may be raised by events

Event Class | Description
--- | ---
`Network | BGP | Prefix Limit Exceeded` | dispose

### Closing Events
`Network | BGP | Prefix Limit Exceeded` may be cleared by events

Event Class | Description
--- | ---
`Network | BGP | Established` | dispose
`Network | BGP | Peer State Changed` | clear_maxprefix
