# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS.get_interface_status test
## Auto-generated by manage.py debug-script at 2011-05-03 13:33:22
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Zyxel_ZyNOS_get_interface_status_Test(ScriptTestCase):
    script = "Zyxel.ZyNOS.get_interface_status"
    vendor = "Zyxel"
    platform='ES-2024A'
    version='3.90(TX.1)'
    input = {'interface': 10}
    result = [{'interface': '10', 'status': True}]
    motd = ' **********\nCopyright (c) 1994 - 2007 ZyXEL Communications Corp.\n'
    cli = {
## 'show interfaces 10'
'show interfaces 10': """ show interfaces 10
  Port Info\tPort NO.\t\t:10
  \t\tLink\t\t\t:100M/F Copper
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:852150866
  \t\tRxPkts\t\t\t:889143201
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:294.344
  \t\tRx KBs/s\t\t:21.741
  \t\tUp Time\t\t\t:185:48:41
  TX Packet\tTx Packets\t\t:852150866
  \t\tMulticast\t\t:6636832
  \t\tBroadcast\t\t:1282374
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:849639255
  RX Packet\tRx Packets\t\t:889143201
  \t\tMulticast\t\t:520342
  \t\tBroadcast\t\t:188448
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
 \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:2444805
  \t\t65 to 127\t\t:713200987
  \t\t128 to 255\t\t:82041659
  \t\t256 to 511\t\t:38081043
  \t\t512 to 1023\t\t:54854916
  \t\t1024 to 1518\t\t:676647915
  \t\tGiant\t\t\t:1
  """, 
}
    snmp_get = {}
    snmp_getnext = {}
