---
uuid: 53b4f0da-3915-4573-adc3-3084a22e5516
---
# Vendor | Cisco | SCOS | Security | Attack | Attack Detected

## Symptoms

Possible DoS/DDoS traffic from source

## Probable Causes

Virus/Botnet activity or malicious actions

## Recommended Actions

Negotiate the source if it is your customer, or ignore

## Variables

Variable | Description | Default
--- | --- | ---
from_ip | From IP | `:material-close:`
to_ip | To IP | `:material-close:`
from_side | From Side | `:material-close:`
proto | Protocol | `:material-close:`
open_flows | Open Flows | `:material-close:`
suspected_flows | Suspected Flows | `:material-close:`
action | Action | `:material-close:`

## Events

### Opening Events
`Vendor | Cisco | SCOS | Security | Attack | Attack Detected` may be raised by events

Event Class | Description
--- | ---
`Vendor | Cisco | SCOS | Security | Attack | Attack Detected` | Attack Detected

### Closing Events
`Vendor | Cisco | SCOS | Security | Attack | Attack Detected` may be cleared by events

Event Class | Description
--- | ---
`Vendor | Cisco | SCOS | Security | Attack | End-of-attack detected` | Clear Attack Detected
