---
uuid: dcb43df5-cca3-4945-b3f1-b7d4140fdb4e
---
# Security | Attack | Attack

Attack in progress detected

## Symptoms

Unsolicitized traffic from source

## Probable Causes

Virus/Botnet activity or malicious actions

## Recommended Actions

Negotiate the source if it is your customer, or ignore

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
name | str | :material-close: | Attack name
interface | interface_name | :material-check: | Interface
src_ip | ip_address | :material-check: | Source IP
src_mac | mac | :material-check: | Source MAC
vlan | int | :material-check: | Vlan ID

## Alarms

### Raising alarms

`Security | Attack | Attack` events may raise following alarms:

Alarm Class | Description
--- | ---
`Security | Attack | Attack` | dispose
