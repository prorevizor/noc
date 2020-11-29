# cfgtrap DataStream

`cfgtrap` [DataStream](index.md) contains configuration
for :ref:`services-trapcollector<trapcollector>` service

## Fields

| Name      | Type            | Description                                                |
| --------- | --------------- | ---------------------------------------------------------- |
| id        | String          | :ref:`Managed Object's<reference-managed-object>` id       |
| change_id | String          | [Record's Change Id](index.md#change-id)                   |
| pool      | String          | :ref:`Pool's name<reference-pool>`                         |
| fm_pool   | String          | :ref:`Pool's name<reference-pool>` for FM event processing |
| addresses | Array of String | List of SNMP Trap sources' IP addresses                    |

## Filters

### pool(name)

Restrict stream to objects belonging to pool `name`

name
: Pool name

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:cfgtrap` permissions
required.
