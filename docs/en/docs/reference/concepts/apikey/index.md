# API Key

## Usage
Client *MUST* set `Private-Token` HTTP Request header and set it
with proper *Key* in order to get access to protected API

Example: `curl  -s -D - -k -H 'Private-Token: 12345'  https://noc_url/api/datastream/managedobject` ,
where 12345 is an API token key.

## Roles

### DataStream API
Access to [DataStream API](../../../api/datastream/index.md)

API:Role | Description
-------- | -----------
`datastream:administrativedomain` | [administrativedomain DataStream](../../../api/datastream/administrativedomain.md)
`datastream:alarm` | [administrativedomain DataStream](../../../api/datastream/alarm.md)
`datastream:resourcegroup` | [resourcegroup DataStream](../../../api/datastream/resourcegroup.md)
`datastream:managedobject` | [managedobject DataStream](../../../api/datastream/managedobject.md)

+-----------------------------------+------------------------------------------------------------------------------------+
| `datastream:dnszone`              | :ref:`dnszone datastream <api-datastream-dnszone>` access                          |
+-----------------------------------+------------------------------------------------------------------------------------+
| `datastream:cfgping`              | :ref:`cfgping datastream <api-datastream-cfgping>` access                          |
+-----------------------------------+------------------------------------------------------------------------------------+
| `datastream:cfgsyslog`            | :ref:`cfgsyslog datastream <api-datastream-cfgsyslog>` access                      |
+-----------------------------------+------------------------------------------------------------------------------------+
| `datastream:cfgtrap`              | :ref:`cfgtrap datastream <api-datastream-cfgtrap>` access                          |
+-----------------------------------+------------------------------------------------------------------------------------+
| `datastream:vrf`                  | :ref:`vrf datastream <api-datastream-vrf>` access                                  |
+-----------------------------------+------------------------------------------------------------------------------------+
| `datastream:prefix`               | :ref:`prefix datastream <api-datastream-prefix>` access                            |
+-----------------------------------+------------------------------------------------------------------------------------+
| `datastream:address`              | :ref:`address datastream <api-datastream-address>` access                          |
+-----------------------------------+------------------------------------------------------------------------------------+

### NBI API

+-----------------------+----------------------------------------------------------------+
| API:Role              | Description                                                    |
+=======================+================================================================+
| `nbi:config`          | :ref:`NBI config API <api-nbi-config>` access                  |
+-----------------------+----------------------------------------------------------------+
| `nbi:configrevisions` | :ref:`NBI configrevisions API <api-nbi-configrevisions>` access|
+-----------------------+----------------------------------------------------------------+
| `nbi:getmappings`     | :ref:`NBI getmappings API <api-nbi-getmappings>` access        |
+-----------------------+----------------------------------------------------------------+
| `nbi:objectmetrics`   | :ref:`NBI objectmetrics API <api-nbi-objectmetrics>` access    |
+-----------------------+----------------------------------------------------------------+
| `nbi:objectstatus`    | :ref:`NBI objectstatus API <api-nbi-objectstatus>` access      |
+-----------------------+----------------------------------------------------------------+
| `nbi:path`            | :ref:`NBI path API <api-nbi-path>` access                      |
+-----------------------+----------------------------------------------------------------+
| `nbi:telemetry`       | :ref:`NBI telemetry API <api-nbi-telemetry>` access            |
+-----------------------+----------------------------------------------------------------+

## Web interface example
You should fill `Name` and `API key` as required fields.
Also in `API` rows should be `nbi`  or `datastream`. In `Role` row should be a role from tables above or `*` (asterisk)

![Edit API](edit_api.png)

You can fill the ACL section or may leave it empty.
Prefix field should be in a IP/net way.

![Edit API ACL](edit_api_acl.png)

Also there is an opportunity to allow requests to API only from whitelist IPs.
You can find this option in Tower, in `nbi`/`datastream` service respectively.

## Best Practices
* Grant separate API Keys for every connected system
* Grant separate API Keys for every developer, Restrict key lifetime
* Grant separate API Keys for every external tester, Restrict key to short lifetime
