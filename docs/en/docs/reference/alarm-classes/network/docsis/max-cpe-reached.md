---
uuid: 69fd89a2-85eb-4be1-a8c4-2ee20c301ea4
---
# Network | DOCSIS | Max CPE Reached

## Symptoms

## Probable Causes

The maximum number of devices that can be attached to the cable modem has been exceeded. Therefore, the device with the specified IP address will not be added to the modem with the specified SID.

## Recommended Actions

Locate the specified device and place the device on a different cable modem with another SID.

## Variables

Variable | Description | Default
--- | --- | ---
mac | CPE MAC | `:material-close:`
ip | CPE IP | `:material-close:`
modem_mac | Cable Modem MAC | `:material-close:`
sid | Cable Modem SID | `:material-close:`
interface | Cable interface | `:material-close:`

## Events

### Opening Events
`Network | DOCSIS | Max CPE Reached` may be raised by events

Event Class | Description
--- | ---
`Network | DOCSIS | Max CPE Reached` | dispose
