---
uuid: 70c6f606-e6eb-423a-86fb-87f0d6821f19
---
# NOC | SA | Activator Pool Degraded

## Symptoms

Cannot run SA tasks. Too many timeout errors

## Probable Causes

noc-activator processes down

## Recommended Actions

Check noc-activator processes. Check network connectivity

## Variables

Variable | Description | Default
--- | --- | ---
name | Pool Name | `:material-close:`

## Events

### Opening Events
`NOC | SA | Activator Pool Degraded` may be raised by events

Event Class | Description
--- | ---
`NOC | SA | Leave Activator Pool` | raise
`NOC | SA | Join Activator Pool` | raise

### Closing Events
`NOC | SA | Activator Pool Degraded` may be cleared by events

Event Class | Description
--- | ---
`NOC | SA | Leave Activator Pool` | clear
`NOC | SA | Join Activator Pool` | clear
