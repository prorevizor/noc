# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES35xx.get_lldp_neighbors test
## Auto-generated by manage.py debug-script at 2010-09-24 17:48:01
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES35xx_get_lldp_neighbors_Test(ScriptTestCase):
    script="EdgeCore.ES35xx.get_lldp_neighbors"
    vendor="EdgeCore"
    platform='ES3526XA-V2'
    version='1.1.0.29'
    input={}
    result=[{'local_interface': 'Eth 1/26',
  'local_interface_id': '00:12:CF:90:C8:DA',
  'neighbors': [{'remote_capabilities': 20,
                 'remote_chassis_id': '00:26:88:70:7F:00',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '143',
                 'remote_port_subtype': 7,
                 'remote_system_name': 'Jun3200_Shotkina8_2'}]}]
    motd=' \n\n      CLI session with the ES3526XA is opened.\n      To end the CLI session, enter [Exit].\n\n'
    cli={
## 'show lldp info remote detail Eth 1/26'
'show lldp info remote detail Eth 1/26': """show lldp info remote detail Eth 1/26

 LLDP Remote Devices Information Detail

---------------------------------------------------------------
  Local PortName     : Eth 1/26
  Chassis Type       : MAC Address
  Chassis Id         : 00-26-88-70-7F-00 
  PortID Type        : Local
  PortID             : 31-34-33-00-00-00
  SysName            : Jun3200_Shotkina8_2
  SysDescr           : Juniper Networks, Inc. ex3200-24t , version 10.0S1.1 B
                       uild date: 2010-01-08 06:46:50 UTC 
  PortDescr          : ge-0/0/16.0
  SystemCapSupported : Bridge, Router  
  SystemCapEnabled   : Bridge, Router  
  Remote VLAN Name : 
    VLAN-3120 : vl3120
    VLAN-3777 : vl3777
  Remote MAC/PHY configuration status :
    Remote port auto-neg supported : Yes
    Remote port auto-neg enabled : Yes
    Remote port auto-neg advertised cap (Hex) : A836
    Remote port MAU type : 0
  Remote Link Aggregation : 
    Remote link aggregation capable : Yes
    Remote link aggragation enable : No
  Remote link aggragation port id : 0
  Remote Max Frame Size : 1514
""",
## 'show lldp info remote-device'
'show lldp info remote-device': """show lldp info remote-device

 LLDP Remote Devices Information

  Interface | ChassisId         PortId            SysName              
  --------- + ----------------- ----------------- ---------------------
  Eth 1/26  | 00-26-88-70-7F-00 31-34-33-00-00-00 Jun3200_Shotkina8...
""",
## 'show lldp info local-device'
'show lldp info local-device': """show lldp info local-device

 LLDP Local System Information
  Chassis Type : MAC Address
  Chassis ID   : 00-12-CF-90-C8-C0
  System Name  : Terkina54-1
  System Description : Layer2+ Fast Ethernet Standalone Switch ES3526XA
  System Capabilities Support : Bridge
  System Capabilities Enable  : Bridge
  Management Address : 10.254.2.103 (IPv4)

 LLDP Port Information
  Port  | PortID Type      PortID            PortDesc
  ----- + ---------------- ----------------- --------------------------------
 Eth1/1 | MAC Address      00-12-CF-90-C8-C1 Ethernet Port on unit 1, port 1 
 Eth1/2 | MAC Address      00-12-CF-90-C8-C2 Ethernet Port on unit 1, port 2 
 Eth1/3 | MAC Address      00-12-CF-90-C8-C3 Ethernet Port on unit 1, port 3 
 Eth1/4 | MAC Address      00-12-CF-90-C8-C4 Ethernet Port on unit 1, port 4 
 Eth1/5 | MAC Address      00-12-CF-90-C8-C5 Ethernet Port on unit 1, port 5 
 Eth1/6 | MAC Address      00-12-CF-90-C8-C6 Ethernet Port on unit 1, port 6 
 Eth1/7 | MAC Address      00-12-CF-90-C8-C7 Ethernet Port on unit 1, port 7 
 Eth1/8 | MAC Address      00-12-CF-90-C8-C8 Ethernet Port on unit 1, port 8 
 Eth1/9 | MAC Address      00-12-CF-90-C8-C9 Ethernet Port on unit 1, port 9 
 Eth1/10| MAC Address      00-12-CF-90-C8-CA Ethernet Port on unit 1, port 10
 Eth1/11| MAC Address      00-12-CF-90-C8-CB Ethernet Port on unit 1, port 11
 Eth1/12| MAC Address      00-12-CF-90-C8-CC Ethernet Port on unit 1, port 12
 Eth1/13| MAC Address      00-12-CF-90-C8-CD Ethernet Port on unit 1, port 13
 Eth1/14| MAC Address      00-12-CF-90-C8-CE Ethernet Port on unit 1, port 14
 Eth1/15| MAC Address      00-12-CF-90-C8-CF Ethernet Port on unit 1, port 15
 Eth1/16| MAC Address      00-12-CF-90-C8-D0 Ethernet Port on unit 1, port 16
 Eth1/17| MAC Address      00-12-CF-90-C8-D1 Ethernet Port on unit 1, port 17
 Eth1/18| MAC Address      00-12-CF-90-C8-D2 Ethernet Port on unit 1, port 18
 Eth1/19| MAC Address      00-12-CF-90-C8-D3 Ethernet Port on unit 1, port 19
 Eth1/20| MAC Address      00-12-CF-90-C8-D4 Ethernet Port on unit 1, port 20
 Eth1/21| MAC Address      00-12-CF-90-C8-D5 Ethernet Port on unit 1, port 21
 Eth1/22| MAC Address      00-12-CF-90-C8-D6 Ethernet Port on unit 1, port 22
 Eth1/23| MAC Address      00-12-CF-90-C8-D7 Ethernet Port on unit 1, port 23
 Eth1/24| MAC Address      00-12-CF-90-C8-D8 Ethernet Port on unit 1, port 24
 Eth1/25| MAC Address      00-12-CF-90-C8-D9 Ethernet Port on unit 1, port 25
 Eth1/26| MAC Address      00-12-CF-90-C8-DA Ethernet Port on unit 1, port 26""",
}
    snmp_get={}
    snmp_getnext={}
