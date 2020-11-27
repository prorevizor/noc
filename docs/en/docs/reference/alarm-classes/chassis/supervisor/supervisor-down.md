---
uuid: e4faaa3f-e50c-4eb2-a420-5ec5143e6512
---
# Chassis | Supervisor | Supervisor Down

## Symptoms

## Probable Causes

## Recommended Actions

## Variables

Variable | Description | Default
--- | --- | ---
name | Supervisor name | `:material-close:`
reason | Reason | `:material-close:`

## Alarm Correlation

Scheme of correlation of `Chassis | Supervisor | Supervisor Down` alarms with other alarms is on the chart. 
Arrows are directed from root cause to consequences.

```mermaid
graph TD
  A[["Chassis | Supervisor | Supervisor Down"]]
  C1["Config | Config Sync Failed"]
  A --> C1
```

### Root Causes
`Chassis | Supervisor | Supervisor Down` alarm may be root cause of

Alarm Class | Description
--- | ---
`Config | Config Sync Failed` | Supervisor Down

## Events

### Opening Events
`Chassis | Supervisor | Supervisor Down` may be raised by events

Event Class | Description
--- | ---
`Chassis | Supervisor | Supervisor Down` | dispose

### Closing Events
`Chassis | Supervisor | Supervisor Down` may be cleared by events

Event Class | Description
--- | ---
`Chassis | Supervisor | Supervisor Up` | dispose
