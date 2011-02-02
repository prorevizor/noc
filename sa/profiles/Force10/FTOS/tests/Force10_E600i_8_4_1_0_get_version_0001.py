# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Force10.FTOS.get_version test
## Auto-generated by manage.py debug-script at 2011-02-02 14:06:34
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Force10_FTOS_get_version_Test(ScriptTestCase):
    script="Force10.FTOS.get_version"
    vendor="Force10"
    platform='E600i'
    version='8.4.1.0'
    input={}
    result={'platform': 'E600i', 'vendor': 'Force10', 'version': '8.4.1.0'}
    motd=' \n'
    cli={
## 'show version'
'show version': """show version
Force10 Networks Real Time Operating System Software
Force10 Operating System Version: 1.0
Force10 Application Software Version: 8.4.1.0
Copyright (c) 1999-2010 by Force10 Networks, Inc.
Build Time: Mon Nov 8 13:06:55 2010
Build Path: /sites/sjc/work/build/buildSpaces/build11/E8-4-1/SW/SRC
sw-1-x2 uptime is 1 day(s), 3 hour(s), 23 minute(s)

System image file is "flash://FTOS-EH-8.4.1.0.bin"

Chassis Type: E600i 
Control Processor: IBM PowerPC 750FX (Rev D2.2) with 1073741824 bytes of memory.
Route Processor 1: IBM PowerPC 750FX (Rev D2.2) with 1073741824 bytes of memory.
Route Processor 2: IBM PowerPC 750FX (Rev D2.2) with 1073741824 bytes of memory.

128K bytes of non-volatile configuration memory.

  2 Route Processor Module
  5 Switch Fabric Module
  2 90-port 10/100/1000Base-T line card with mini RJ-21 interfaces 10M CAM (EH)
  4 10-port 10GE LAN/WAN PHY line card with SFP+ options 10M CAM (EH)
  2 FastEthernet/IEEE 802.3 interface(s)
180 GigabitEthernet/IEEE 802.3 interface(s)
 40 Ten GigabitEthernet/IEEE 802.3 interface(s)""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
