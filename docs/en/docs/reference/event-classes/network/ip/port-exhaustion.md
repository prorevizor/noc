---
uuid: c10a55e0-29ed-44ae-89b1-0d6019a23bd7
---
# Network | IP | Port Exhaustion

Port Exchaustion

## Symptoms

Failed to establish outgoung connection

## Probable Causes

No free TCP/UDP ports for outgoung connection

## Recommended Actions

Check applications and aging intervals

## Variables

Variable | Type | Required | Description
--- | --- | --- | ---
src_ip | ip_address | :material-check: | Source address
dst_ip | ip_address | :material-check: | Destination address
dst_port | int | :material-check: | Destination port
proto | int | :material-check: | Protocol
