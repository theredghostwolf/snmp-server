#libs

import time
from pysnmp.hlapi import *
import os

#variables

HtmlFile = "index.html"
SwitchList = "switches.txt"
refreshDelay = 60 #in seconds
requestTimeOut = 161
switchStartupConfigFolder = "test"

#code and stuff

while True:
    SwitchFile = open(SwitchList, "r")
    content = SwitchFile.readlines()
    SwitchFile.close()
    htmlFile = open(HtmlFile, "w")
    for x in content:
        x = x.split(',')
        ip = x[0].strip()

        if x[1] is not None:
            txt = x[1].strip().strip("\n")

        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData('public', mpModel=0),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
            )

        htmlString = ""
        htmlString += ip + " : "
        if errorIndication:
            htmlString += str(errorIndication)
        elif errorStatus:
            htmlString += errorStatus.prettyPrint()
        else:
            for s in varBinds:
                s = str(s)
                s.replace(",", " <br> ")
                htmlString += s + " <br> "

        htmlFile.write(htmlString + " <br> <br>")

        if txt is not None:
            switchStartupFile = open(switchStartupConfigFolder + "/" + txt, 'r')
            c = switchStartupFile.readlines()
            switchStartupFile.close()
            for z in c:
                htmlFile.write(z + " <br> ")

            htmlFile.write(" <br> ")

    htmlFile.close()
    print("updated file...")
    time.sleep(refreshDelay)
