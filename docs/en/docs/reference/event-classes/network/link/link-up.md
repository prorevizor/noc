---
uuid: 82d72502-974a-4c42-8fe4-c4d2aae71d5c
---
# Network | Link | Link Up

Link Up

## Symptoms

Connection restored

## Probable Causes

Administrative action, cable or hardware replacement

## Recommended Actions

Check interfaces on both sides for possible errors

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
interface | interface_name | :material-close: | Affected interface
speed | str | :material-check: | Link speed
duplex | str | :material-check: | Duplex mode

## Alarms

### Clearing alarms

`Network | Link | Link Up` events may clear following alarms:

Alarm Class | Description
--- | ---
`Network | Link | Link Down` | Clear Link Down
`Network | Link | Err-Disable` | Clear Err-Disable
`Network | STP | BPDU Guard Violation` | Clear BPDU Guard Violation
`Network | STP | Root Guard Violation` | Clear Root Guard Violation
