#libs

import time
from pysnmp.hlapi import *
import os

#variables

HtmlFile = "index.html"
SwitchList = "switches.txt"
refreshDelay = 60 #in seconds
requestTimeOut = 161

#code and stuff

while True:
    SwitchFile = open(SwitchList, "r")
    content = SwitchFile.readlines()
    SwitchFile.close()
    htmlFile = open(HtmlFile, "w")
    for x in content:
        x.strip()
        x.strip('\n')

        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData('public', mpModel=0),
                UdpTransportTarget((x, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
            )

        htmlString = ""
        htmlString += x + " : "
        if errorIndication:
            htmlString += str(errorIndication)
        elif errorStatus:
            htmlString += errorStatus.prettyPrint()
        else:
            for s in varBinds:
                htmlString += s + " "

        htmlFile.write(htmlString + " <br>")

    htmlFile.close()
    print("updated file...")
    time.sleep(refreshDelay)
