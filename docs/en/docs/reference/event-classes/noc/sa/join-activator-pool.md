---
uuid: 2aaf7e96-8221-44e0-bc49-aa82b3bb20bd
---
# NOC | SA | Join Activator Pool

## Symptoms

SA performance increased

## Probable Causes

noc-activator process been launched

## Recommended Actions

No recommended actions

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
name | str | :material-close: | Activator pool name
instance | str | :material-close: | Activator instance
sessions | int | :material-close: | Instance's script sessions
min_members | int | :material-close: | Pool's members lower threshold
min_sessions | int | :material-close: | Pool's sessions lower threshold
pool_members | int | :material-close: | Pool's current members
pool_sessions | int | :material-close: | Pool's current sessions limit

## Alarms

### Raising alarms

`NOC | SA | Join Activator Pool` events may raise following alarms:

Alarm Class | Description
--- | ---
`NOC | SA | Activator Pool Degraded` | raise

### Clearing alarms

`NOC | SA | Join Activator Pool` events may clear following alarms:

Alarm Class | Description
--- | ---
`NOC | SA | Activator Pool Degraded` | clear
