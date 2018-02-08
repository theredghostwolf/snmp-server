#libs

import time
from pysnmp.hlapi import *
import os
import os.path

#variables

HtmlFile = "index.html"
SwitchList = "switches.txt"
refreshDelay = 60 #in seconds
requestTimeOut = 161
switchStartupConfigFolder = "test"

#code and stuff

def writeHtmlHeader(f):
    f.write('<head>  <link rel="stylesheet" href="main.css" media="screen" title="no title">  <script src="main.js"></script>  </head>')


while True:
    SwitchFile = open(SwitchList, "r")
    content = SwitchFile.readlines()
    SwitchFile.close()
    htmlFile = open(HtmlFile, "w")

    writeHtmlHeader(htmlFile);
    index = 0


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

        htmlFile.write(htmlString + " <button onclick='toggleDiv( " + str(index) + ")'> show config </button> <br> <br>")

        if txt is not None:
            path = switchStartupConfigFolder + "/" + txt
            if os.path.isfile(path):
                switchStartupFile = open(path, 'r')
                c = switchStartupFile.readlines()
                switchStartupFile.close()
                for z in c:
                    htmlFile.write("<div id='" + str(index) + "' style='display:none'>" + z + " <br> </div> ")

                htmlFile.write(" <br> ")

        index = index + 1

    htmlFile.close()
    print("updated file...")
    time.sleep(refreshDelay)
