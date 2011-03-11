# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_version test
## Auto-generated by manage.py debug-script at 2011-03-11 15:24:35
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class DLink_DxS_get_version_Test(ScriptTestCase):
    script="DLink.DxS.get_version"
    vendor="DLink"
    platform='DES-3852'
    version='4.50.B12'
    input={}
    result={'platform': 'DES-3852', 'vendor': 'DLink', 'version': '4.50.B12'}
    motd='******\n\n'
    cli={
## 'show switch'
'show switch': """show switch
Command: show switch

Device Type       : DES-3852 Fast-Ethernet Switch
Combo Port Type   : 1000Base-T + 1000Base-T
MAC Address       : 00-13-46-7F-E5-40
IP Address        : 10.10.10.253 (Manual)
VLAN Name         : default
Subnet Mask       : 255.255.255.0
Default Gateway   : 0.0.0.0
Boot PROM Version : Build 0.00.008
Firmware Version  : Build 4.50.B12
Hardware Version  : 1A1
Serial Number     : 
Power Status      : Main - Normal, Redundant - Not Present
System Name       : 
System Location   : 
System Contact    : 
Spanning Tree     : Disabled
GVRP              : Disabled
IGMP Snooping     : Disabled
MLD Snooping      : Disabled
TELNET            : Enabled (TCP 23)
SSH               : Disabled
WEB               : Enabled (TCP 80)
RMON              : Disabled
RIP               : Disabled
DVMRP             : Disabled
PIM               : Disabled
OSPF              : Disabled
SNMP              : Disabled
""",
## 'disable clipaging'
'disable clipaging': """disable clipaging
Command: disable clipaging

Success.   
""",
}
    snmp_get={}
    snmp_getnext={}
