---
uuid: c720e355-84dd-44a2-b7fd-5cb4f6ca5f0e
---
# Network | EIGRP | Neighbor Down

EIGRP adjacency down

## Symptoms

Routing table changes and possible lost of connectivity

## Probable Causes

Link failure or protocol misconfiguration

## Recommended Actions

Check links and local and neighbor router configuration

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
as | str | :material-check: | EIGRP automonus system
interface | str | :material-close: | Interface
neighbor | ip_address | :material-close: | Neighbor's Router ID
reason | str | :material-check: | Adjacency lost reason
to_state | str | :material-check: | to state

## Alarms

### Raising alarms

`Network | EIGRP | Neighbor Down` events may raise following alarms:

Alarm Class | Description
--- | ---
`Network | EIGRP | Neighbor Down` | dispose
