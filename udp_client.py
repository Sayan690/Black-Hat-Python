#!/usr/bin/python2

import sys
import socket

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto("AAABBBCCCDDDEEE696969", (host, port))

data, addr = s.recv(4096)
print data
s.close()