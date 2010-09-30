from Socket import *
import simplejson as json

sckt = Socket()
sckt._connect('localhost',13854)
msg = {"appName":"testApp", "appKey":"b5b8b5374f7649ce322647506a80c30e2deb87cc"}
print "authenticating..."
sckt._send(msg)
reply = sckt._receive()
print ("authentication reply: %s") %reply

msg = {"enableRawOutput": true, "format": "Json"}
print "configuring..."
sckt._send(msg)