#libs

import time
from pysnmp.hlapi import *
import os
import os.path
import datetime

#variables

HtmlFile = "index.html"
SwitchList = "switches.txt"
refreshDelay = 60 #in seconds
requestTimeOut = 161
switchStartupConfigFolder = "test"
latestStartupConfigFolder = "test2"

#code and stuff

def checkFiles():
    if not os.path.isdir(switchStartupConfigFolder):
        os.mkdir(switchStartupConfigFolder)

    if not os.path.isdir(latestStartupConfigFolder):
        os.mkdir(latestStartupConfigFolder)

def cleanupStartupFiles():
    fList = os.listdir(switchStartupConfigFolder)
    finalList = []

    for x in fList:
        f = x
        f = f.split("-")
        f = list(filter(None, f))

        stamp = f[1] + ":" + f[2] + ":" + f[3] + ":" + f[4]  + ":" + f[5]

        t = datetime.datetime.strptime(stamp, "%b:%d:%H:%M:%S.%f")

        finalList.append([f[0], t, x])


    types = []

    for x in finalList:
        added = False
        for z in types:
            if z[0] == x[0]:
                z[1].append(x)
                added = True

        if not added:
            types.append([x[0], [x]])


    for t in types:
        times = []
        for f in t[1]:
            times.append(f[1])

        newest = max(dt for dt in times)


        for f in t[1]:
            if f[1] == newest:
                old = open(switchStartupConfigFolder + "/" + f[2], 'r')
                new = open(latestStartupConfigFolder + "/" + f[0], 'w')

                oldContent = old.read()
                new.write(oldContent)

                old.close()
                new.close()
            else:
                os.remove(switchStartupConfigFolder + "/" + f[2])

    print("cleaned-up files")

def writeHtmlHeader(f):
    f.write('<head>  <link rel="stylesheet" href="main.css" media="screen" title="no title">  <script src="main.js"></script>  </head>')


checkFiles()
while True:
    cleanupStartupFiles()

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
            path = latestStartupConfigFolder + "/" + txt
            if os.path.isfile(path):
                switchStartupFile = open(path, 'r')
                c = switchStartupFile.readlines()
                switchStartupFile.close()
                htmlFile.write("<div id='" + str(index) + "' style='display:none'>")
                for z in c:
                    htmlFile.write(z + " <br>")

                htmlFile.write("</div> <br> ")

        index = index + 1

    htmlFile.close()
    print("updated file...")
    time.sleep(refreshDelay)
