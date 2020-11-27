---
uuid: 20d3c3e7-1c33-458d-9e12-837670bbd080
---
# Network | STP | BPDU Guard Violation

## Symptoms

## Probable Causes

## Recommended Actions

## Variables

Variable | Description | Default
--- | --- | ---
interface | interface | `:material-close:`
description | Interface description | `=InterfaceDS.description`

## Events

### Opening Events
`Network | STP | BPDU Guard Violation` may be raised by events

Event Class | Description
--- | ---
`Network | STP | BPDU Guard Violation` | dispose

### Closing Events
`Network | STP | BPDU Guard Violation` may be cleared by events

Event Class | Description
--- | ---
`Network | STP | BPDU Guard Recovery` | dispose
`Network | Link | Link Up` | Clear BPDU Guard Violation
