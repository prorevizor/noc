# resourcegroup DataStream

`resourcegroup` [DataStream](index.md) contains summarized :ref:`Resource Group<reference-resource-group>`
state

## Fields

| Name           | Type                 | Description                                                        |
| -------------- | -------------------- | ------------------------------------------------------------------ |
| id             | String               | :ref:`Administrative Domain's<reference-administrative-domain>` ID |
| name           | String               | Name                                                               |
| parent         | String               | Parent's ID (if exists)                                            |
| technology     | Object {{ complex }} | Resource Group's :ref:`Technology<reference-technology>`           |
| remote_system  | Object {{ complex }} | Source :ref:`remote system<reference-remote-system>` for object    |
| {{ tab }} id   | String               | External system's id                                               |
| {{ tab }} name | String               | External system's name                                             |
| remote_id      | String               | External system's id (Opaque attribute)                            |

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:resourcegroup` permissions
required.
