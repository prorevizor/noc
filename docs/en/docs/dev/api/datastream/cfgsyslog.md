# cfgsyslog DataStream

`cfgsyslog` [DataStream](index.md) contains configuration
for :ref:`syslogcollector<services-syslogcollector>` service

## Fields

| Name      | Type            | Description                                                |
| --------- | --------------- | ---------------------------------------------------------- |
| id        | String          | :ref:`Managed Object's<reference-managed-object>` id       |
| change_id | String          | [Record's Change Id](index.md#change-id)                   |
| pool      | String          | :ref:`Pool's name<reference-pool>`                         |
| fm_pool   | String          | :ref:`Pool's name<reference-pool>` for FM event processing |
| addresses | Array of String | List of syslog sources' IP addresses                       |

## Filters

### pool(name)

Restrict stream to objects belonging to pool `name`

name
: Pool name

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:cfgsyslog` permissions
required.
