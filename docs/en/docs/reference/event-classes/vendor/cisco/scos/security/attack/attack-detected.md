---
uuid: f80e3686-bd0c-4247-afcf-d79cf60cb832
---
# Vendor | Cisco | SCOS | Security | Attack | Attack Detected

Attack detected

## Symptoms

Possible DoS/DDoS traffic from source

## Probable Causes

Virus/Botnet activity or malicious actions

## Recommended Actions

Negotiate the source if it is your customer, or ignore

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
from_ip | ip_address | :material-close: | From IP
to_ip | ip_address | :material-check: | To IP
from_side | str | :material-close: | From Side
proto | str | :material-close: | Protocol
open_flows | int | :material-close: | Open Flows
suspected_flows | int | :material-close: | Suspected Flows
action | str | :material-close: | Action

## Alarms

### Raising alarms

`Vendor | Cisco | SCOS | Security | Attack | Attack Detected` events may raise following alarms:

Alarm Class | Description
--- | ---
`Vendor | Cisco | SCOS | Security | Attack | Attack Detected` | Attack Detected
