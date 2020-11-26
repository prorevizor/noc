---
uuid: ec6f4a1c-6efa-496b-93a7-e591496053e6
---
# Security | ACL | ACL Deny

Packet denied by ACL

## Symptoms

## Probable Causes

## Recommended Actions

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
name | str | :material-check: | ACL Name
proto | str | :material-check: | Protocol
src_interface | interface_name | :material-check: | Source Interface
src_ip | ip_address | :material-check: | Source IP
src_port | int | :material-check: | Source port
src_mac | mac | :material-check: | Source MAC
dst_interface | interface_name | :material-check: | Destination Interface
dst_ip | ip_address | :material-check: | Destination IP
dst_port | int | :material-check: | Destination port
count | int | :material-check: | Packets count
flags | str | :material-check: | Flags
