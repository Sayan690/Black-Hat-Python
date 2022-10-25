#!/usr/bin/python2

import sys
import socket
import argparse
import threading

class TCP_Proxy:
	def __init__(self):
		self.main()

	def main(self):
		# creating the command line args

		parser = argparse.ArgumentParser(description="TCP Proxy.", usage="./%(prog)s [options]", epilog="Example: ./%(prog)s [RHOST] [RPORT]")
		parser.add_argument(metavar="RHOST", help="Remote host ip address.", dest="rhost")
		parser.add_argument(metavar="RPORT", help="Remote port of the target server.", dest="rport", type=int)
		parser.add_argument("-lhost", help="Localhost ip address.", metavar="", default="127.0.0.1")
		parser.add_argument("-lport", help="Local port to run the proxy.", type=int, default=1337)
		parser.add_argument("-recv", help="Connect and receive data before sending it to the remote host.", choices=["true", "false"], default="true", metavar="")
		parser.add_argument("-timeout", help="Set timeout. (default - 2sec)", metavar="", type=int, default=2)

		self.args = parser.parse_args()

		self.lhost = socket.gethostbyname(self.args.lhost)
		self.rhost = socket.gethostbyname(self.args.rhost)

		self.args.recv = True if self.args.recv == "true" else False

		self.proxy()

	def proxy(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			s.bind((self.lhost, self.args.lport))

		except:
			sys.stderr.write("[!] Failed to listen on %s:%d\n" % (self.lhost, self.args.lport))
			sys.exit()

		print "[*] Listening on %s:%d" % (self.lhost, self.args.lport)
		s.listen(5)

		while True:
			self.c, _ = s.accept()

			# printing the local connection info

			print "[==>] Received connection from %s:%d" % (_[0], _[1])

			# starting a thread to handle the remote host

			proxy = threading.Thread(target=self.proxy_handler)
			proxy.start()

	def proxy_handler(self):
		# connecting to the remote host

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.rhost, self.args.rport))

		# receiving some data if necessary

		if self.args.recv:
			buff = self.recv(self.s)
			if len(buff):
				print "[==>] Received %d bytes from localhost." % len(buff)

			self.hexdump(buff)

			# sending data to the response handler

			buff = self.resp_handler(buff)

			# if we have data, send it to the local client

			if len(buff):
				print "[==>] Sending %d bytes to localhost.." % len(buff)
				self.c.send(buff)

		while True:
			# read from localhost

			buffer = self.recv(self.c)

			if len(buffer):
				print "[==>] Received %d bytes from localhost." % len(buffer)
				
				self.hexdump(buffer)

				# sending it to the response handler

				buffer = self.req_handler(buffer)

				# sending the data to the remote host

				self.s.send(buffer)

				print "[<==] Sent to remote host."

			# receiving the response

			buf = self.recv(self.s)

			if len(buf):
				print "[==>] Received %d bytes from remote." % len(buf)

				self.hexdump(buf)

				# sending it to our response handler

				buf = self.resp_handler(buf)

				# send the response to the local socket

				self.c.send(buf)

				print "[==>] Sent to localhost."

	def hexdump(self, src, length=16):
		result = [] 
		digits = 4 if isinstance(src, unicode) else 2 
		for i in xrange(0, len(src), length): 
			s = src[i:i+length] 
			hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s]) 
			text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s]) 
			result.append( b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text)) 

		print b"\n".join(result)

	def recv(self, conn):
		buf = ""

		conn.settimeout(self.args.timeout)

		try:
			while True:
				data = conn.recv(4096 * 4096)

				if not data:
					break

				buf += data

		except: pass

		return buf

	# modify req for remote host

	def req_handler(self, buf):
		# perform packet modifications
		return buf

	# modify req for remote host

	def resp_handler(self, buf):
		# perform packet modifications
		return buf

if __name__ == '__main__':
	try:
		TCP_Proxy()

	except KeyboardInterrupt:
		sys.exit(0)