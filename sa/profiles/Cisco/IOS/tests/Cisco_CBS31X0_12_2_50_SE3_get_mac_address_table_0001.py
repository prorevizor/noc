# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2010-09-24 17:17:46
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_mac_address_table_Test(ScriptTestCase):
    script="Cisco.IOS.get_mac_address_table"
    vendor="Cisco"
    platform='CBS31X0'
    version='12.2(50)SE3'
    input={}
    result=[{'interfaces': ['Po 1'],
  'mac': '00:01:E8:6D:1D:8F',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Po 1'],
  'mac': '00:01:E8:6D:1D:F3',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Po 1'],
  'mac': '00:01:E8:6D:1F:1C',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Po 1'],
  'mac': '00:01:E8:6D:1F:1C',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['Te 2/0/1'],
  'mac': '00:01:E8:D6:44:1C',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['Po 1'],
  'mac': '00:25:03:30:9F:00',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['Po 1'],
  'mac': '00:25:03:30:D9:00',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['Po 1'],
  'mac': '00:1E:0B:BB:09:D2',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:1F:29:6C:5D:17',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:1F:29:6D:06:71',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:44:81:70',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:47:8B:86',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:47:8B:A2',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:48:6C:B0',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:5B:58:84',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:A8:D2:88',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:AC:54:62',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:AC:D8:B8',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:AC:D8:F4',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['Po 1'],
  'mac': '00:21:5A:DC:3C:40',
  'type': 'D',
  'vlan_id': 3}]
    motd=' \nC\nThe system is a property of Acme Inc.\nPlease disconnect immediately if you are not authorized staff\n\n'
    cli={
## 'show mac address-table'
'show mac address-table': """show mac address-table
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
 All    0100.0ccc.cccc    STATIC      CPU
 All    0100.0ccc.cccd    STATIC      CPU
 All    0180.c200.0000    STATIC      CPU
 All    0180.c200.0001    STATIC      CPU
 All    0180.c200.0002    STATIC      CPU
 All    0180.c200.0003    STATIC      CPU
 All    0180.c200.0004    STATIC      CPU
 All    0180.c200.0005    STATIC      CPU
 All    0180.c200.0006    STATIC      CPU
 All    0180.c200.0007    STATIC      CPU
 All    0180.c200.0008    STATIC      CPU
 All    0180.c200.0009    STATIC      CPU
 All    0180.c200.000a    STATIC      CPU
 All    0180.c200.000b    STATIC      CPU
 All    0180.c200.000c    STATIC      CPU
 All    0180.c200.000d    STATIC      CPU
 All    0180.c200.000e    STATIC      CPU
 All    0180.c200.000f    STATIC      CPU
 All    0180.c200.0010    STATIC      CPU
 All    ffff.ffff.ffff    STATIC      CPU
   1    0001.e86d.1d8f    DYNAMIC     Po1
   1    0001.e86d.1df3    DYNAMIC     Po1
   1    0001.e86d.1f1c    DYNAMIC     Po1
   2    0001.e86d.1f1c    DYNAMIC     Po1
   2    0001.e8d6.441c    DYNAMIC     Te2/0/1
   2    0025.0330.9f00    DYNAMIC     Po1
   2    0025.0330.d900    DYNAMIC     Po1
   3    001e.0bbb.09d2    DYNAMIC     Po1
   3    001f.296c.5d17    DYNAMIC     Po1
   3    001f.296d.0671    DYNAMIC     Po1
   3    0021.5a44.8170    DYNAMIC     Po1
   3    0021.5a47.8b86    DYNAMIC     Po1
   3    0021.5a47.8ba2    DYNAMIC     Po1
   3    0021.5a48.6cb0    DYNAMIC     Po1
   3    0021.5a5b.5884    DYNAMIC     Po1
   3    0021.5aa8.d288    DYNAMIC     Po1
   3    0021.5aac.5462    DYNAMIC     Po1
   3    0021.5aac.d8b8    DYNAMIC     Po1
   3    0021.5aac.d8f4    DYNAMIC     Po1
   3    0021.5adc.3c40    DYNAMIC     Po1
Total Mac Addresses for this criterion: 40""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
