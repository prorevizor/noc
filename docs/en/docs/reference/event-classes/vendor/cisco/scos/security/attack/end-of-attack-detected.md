---
uuid: 44947cd0-638a-4bdf-a1e8-5341249ea5eb
---
# Vendor | Cisco | SCOS | Security | Attack | End-of-attack detected

End-of-attack detected

## Symptoms

## Probable Causes

## Recommended Actions

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
from_ip | ip_address | :material-close: | From IP
to_ip | ip_address | :material-check: | To IP
from_side | str | :material-close: | From Side
proto | str | :material-close: | Protocol
flows | int | :material-close: | Flows
duration | str | :material-close: | Duration
action | str | :material-close: | Action

## Alarms

### Clearing alarms

`Vendor | Cisco | SCOS | Security | Attack | End-of-attack detected` events may clear following alarms:

Alarm Class | Description
--- | ---
`Vendor | Cisco | SCOS | Security | Attack | Attack Detected` | Clear Attack Detected
