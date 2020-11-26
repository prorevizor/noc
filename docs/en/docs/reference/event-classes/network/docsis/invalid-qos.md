---
uuid: 4f8d3fcb-a2f0-4cbb-84c3-b2bad33e1b33
---
# Network | DOCSIS | Invalid QoS

Invalid or unsupported QoS setting

## Symptoms

## Probable Causes

The registration of the specified modem has failed because of an invalid or unsupported QoS setting.

## Recommended Actions

Ensure that the QoS fields in the configuration file are set correctly.

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
mac | mac | :material-close: | Cable Modem MAC
sid | int | :material-check: | Cable Modem SID
interface | interface_name | :material-check: | Cable interface

## Alarms

### Raising alarms

`Network | DOCSIS | Invalid QoS` events may raise following alarms:

Alarm Class | Description
--- | ---
`Network | DOCSIS | Invalid QoS` | dispose
