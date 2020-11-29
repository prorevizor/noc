# cfgping DataStream

`cfgping` [DataStream](index.md) contains configuration
for :ref:`ping<services-ping>` service

## Fields

| Name            | Type    | Description                                                                    |
| --------------- | ------- | ------------------------------------------------------------------------------ |
| id              | String  | :ref:`Managed Object's<reference-managed-object>` id                           |
| change_id       | String  | [Record's Change Id](index.md#change-id)                                       |
| pool            | String  | :ref:`Pool's name<reference-pool>`                                             |
| fm_pool         | String  | :ref:`Pool's name<reference-pool>` for FM event processing                     |
| interval        | Integer | Probing rounds interval in seconds                                             |
| policy          | String  | Probing policy:                                                                |
|                 |         | \* f - Success on first successful try                                         |
|                 |         | \* a - Success only if all tries successful                                    |
| size            | Integer | ICMP Echo-Request packet size                                                  |
| count           | Integer | Probe attempts per round                                                       |
| timeout         | Integer | Probe timeout in seconds                                                       |
| report_rtt      | Boolean | Report :ref:`Ping | RTT<metric-type-ping-rtt>` metric per each round           |
| report_attempts | Boolean | Report :ref:`Ping | Attempts<metric-type-ping-attempts>` metric per each round |
| status          | Null    | Reserved                                                                       |
| name            | String  | [Managed Object's](../../../reference/concepts/managed-object/index.md) name   |
| bi_id           | Integer | [Managed Object's](../../../reference/concepts/managed-object/index.md) BI Id  |

<!-- prettier-ignore -->
!!! todo
    Add BI ID reference

## Filters

### pool(name)

Restrict stream to objects belonging to pool `name`

name
: Pool name

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:cfgping` permissions
required.
