# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_lldp_neighbors test
## Auto-generated by manage.py debug-script at 2010-09-24 19:24:11
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_lldp_neighbors_Test(ScriptTestCase):
    script="Cisco.IOS.get_lldp_neighbors"
    vendor="Cisco"
    platform='C3750'
    version='12.2(40)SE'
    input={}
    result=[{'local_interface': 'Gi 1/0/9',
  'neighbors': [{'remote_capabilities': 20,
                 'remote_chassis_id': '00:26:88:70:7F:00',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '157',
                 'remote_port_subtype': 7,
                 'remote_system_name': 'Jun3200_Shotkina8_2'}]},
 {'local_interface': 'Gi 1/0/4',
  'neighbors': [{'remote_capabilities': 20,
                 'remote_chassis_id': '00:26:88:70:90:00',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '166',
                 'remote_port_subtype': 7,
                 'remote_system_name': 'ex3200_Moskovskaya2b'}]},
 {'local_interface': 'Gi 1/0/8',
  'neighbors': [{'remote_capabilities': 4,
                 'remote_chassis_id': '00:12:CF:90:82:A0',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '00:12:CF:90:82:BA',
                 'remote_port_subtype': 3,
                 'remote_system_name': 'Galaktichesky32'}]}]
    motd=' \n\n'
    cli={
## 'show lldp neighbors Gi1/0/4 detail'
'show lldp neighbors Gi1/0/4 detail': """show lldp neighbors Gi1/0/4 detail


Chassis id: 0026.8870.9000
Port id: 166
Port Description: ge-0/0/1.0
System Name: ex3200_Moskovskaya2b

System Description: 
Juniper Networks, Inc. ex3200-24t , version 10.0S1.1 Build date: 2010-01-08 06:46:50 UTC 

Time remaining: 111 seconds
System Capabilities: B,R
Enabled Capabilities: B,R
Management Addresses - not advertised
Auto Negotiation - supported, enabled
Physical media capabilities:
    10base-T(HD)
    10base-T(FD)
    100base-TX(HD)
    100base-TX(FD)
    Symm, Asym Pause(FD)
    1000baseX(FD)
    1000baseT(FD)
Media Attachment Unit type - not advertised
---------------------------------------------


Total entries displayed: 1
""",
## 'show lldp neighbors'
'show lldp neighbors': """show lldp neighbors

Capability codes:
    (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
    (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other

Device ID           Local Intf     Hold-time  Capability      Port ID
Jun3200_Shotkina8_2 Gi1/0/9        120        B,R             157
ex3200_Moskovskaya2bGi1/0/4        120        B,R             166
Galaktichesky32     Gi1/0/8        120        B               0012.cf90.82ba

Total entries displayed: 3
""",
'terminal length 0':  'terminal length 0\n',
## 'show lldp neighbors Gi1/0/8 detail'
'show lldp neighbors Gi1/0/8 detail': """show lldp neighbors Gi1/0/8 detail


Chassis id: 0012.cf90.82a0
Port id: 0012.cf90.82ba
Port Description: Ethernet Port on unit 1, port 26
System Name: Galaktichesky32

System Description: 
Layer2+ Fast Ethernet Standalone Switch ES3526XA

Time remaining: 95 seconds
System Capabilities: B
Enabled Capabilities: B
Management Addresses:
    IP: 10.0.33.49
Auto Negotiation - not supported
Physical media capabilities - not advertised
Media Attachment Unit type - not advertised
---------------------------------------------


Total entries displayed: 1
""",
## 'show lldp neighbors Gi1/0/9 detail'
'show lldp neighbors Gi1/0/9 detail': """show lldp neighbors Gi1/0/9 detail


Chassis id: 0026.8870.7f00
Port id: 157
Port Description: ge-0/0/23.0
System Name: Jun3200_Shotkina8_2

System Description: 
Juniper Networks, Inc. ex3200-24t , version 10.0S1.1 Build date: 2010-01-08 06:46:50 UTC 

Time remaining: 105 seconds
System Capabilities: B,R
Enabled Capabilities: B,R
Management Addresses - not advertised
Auto Negotiation - supported, enabled
Physical media capabilities:
    10base-T(HD)
    10base-T(FD)
    100base-TX(HD)
    100base-TX(FD)
    Symm, Asym Pause(FD)
    1000baseX(FD)
    1000baseT(FD)
Media Attachment Unit type - not advertised
---------------------------------------------


Total entries displayed: 1
""",
}
    snmp_get={}
    snmp_getnext={}
