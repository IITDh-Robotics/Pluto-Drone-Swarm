from socket import socket
from control.consts import *


class Connection:
	def __init__(self, host="192.168.4.1", port=23):
		self.host = host
		self.port = port

	def connect(self):
		print("Connecting to pluto at " + self.host + ":" + self.port + "...")
		try:
			self.s = socket()
			self.s.connect((self.host, self.port))
			print("Connection successful!")
		except:
			print("Connection failed!")
		
	def send(self, data):
		self.s.send(data)

	def disconnect(self):
		self.s.shutdown(self.SHUT_RDWR)
		self.s.close()
		print("Disconnected from pluto at " + self.host + ":" + self.port + ".")

	def receive(self):
		res = self.s.recv(50)
		res = bytearray(res)
		if DBG_CONN:
			packLen = int.from_bytes(res[3:4], byteorder="little")
			arrLen = len(res)
			for i in range(5, 5+packLen):
				print(f"{hex(res[i])}", end=" ")
			print()
		return res
