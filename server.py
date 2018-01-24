#libs

import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

#variables

IP = ''
PORT = 8080

#stuff you shouldnt touch... probably... i mean i cant stop you

HandlerClass = SimpleHTTPRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = PORT
server_address = (IP, port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
