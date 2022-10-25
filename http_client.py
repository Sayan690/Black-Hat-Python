#!/usr/bin/python2

import sys
import socket

host = sys.argv[1]
try:
	port = int(sys.argv[2])

except IndexError:
	port = 80

try:
	to_send = sys.argv[3]
except IndexError:
	to_send = host

if "-h" in sys.argv or "--help" in sys.argv:
	print "%s [host to connect] [port to connect] [hostname in req]" % sys.argv[0]
	exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send("GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % to_send)
data = s.recv(4096*4096)
print data
s.close()