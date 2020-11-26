---
uuid: 2d7a2484-2918-4117-84cd-294cc0d1375e
---
# Network | DOCSIS | Invalid DOCSIS Message

Invalid DOCSIS Message received from a Cable Modem

## Symptoms

## Probable Causes

A cable modem that is not DOCSIS-compliant has attempted to send an invalid DOCSIS message.

## Recommended Actions

Locate the cable modem that sent this message and replace it with DOCSIS-compliant modem.

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
interface | interface_name | :material-check: | Cable interface
mac | mac | :material-check: | Cable Modem MAC
sid | int | :material-check: | Cable Modem SID

## Alarms

### Raising alarms

`Network | DOCSIS | Invalid DOCSIS Message` events may raise following alarms:

Alarm Class | Description
--- | ---
`Network | DOCSIS | Invalid DOCSIS Message` | dispose
