#!/usr/bin/python2

import socket
import threading

ip = "0.0.0.0"
port = 1337

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ip, port))
server.listen(5)
print "[+] Listening on %s:%d" % (ip, port)

def handle_client(client):
	req = client.recv(1024)
	print "[+] Received: %s" % req

	client.send("ACK!")
	client.close()

while True:
	client, addr = server.accept()
	print "[+] Accepted connection from %s:%d" % (addr[0], addr[1])

	handler = threading.Thread(target=handle_client, args=(client, ))
	handler.start()