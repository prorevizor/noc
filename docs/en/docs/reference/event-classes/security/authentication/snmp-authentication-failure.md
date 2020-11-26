---
uuid: 91094f01-18a3-4fdf-849b-26de6e751b61
---
# Security | Authentication | SNMP Authentication Failure

SNMP authentication failure

## Symptoms

NOC, NMS and monitoring systems cannot interact with the box over SNMP protocol

## Probable Causes

SNMP server is misconfigured, community mismatch, misconfigured ACL or brute-force attack in progress

## Recommended Actions

Check SNMP configuration

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
ip | ip_address | :material-close: | Request source address
community | str | :material-check: | Request SNMP community
