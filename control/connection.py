from socket import socket
from control.consts import *


class Connection:
	def __init__(self, host="192.168.4.1", port=23):
		self.host = host
		self.port = port

	def connect(self):
		print(f"Connecting to pluto at {self.host}:{self.port}...")
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
		print(f"Disconnected from pluto at {self.host}:{self.port}...")

	def receive(self):
		def calculateChecksum(packet):
			checksum = 0
			for byte in bytearray(packet)[3:]:
				checksum ^= byte
			return checksum

		res = bytearray(self.s.recv(50))

		# Check if response is valid
		err = None
		if res[0:3] != bytearray(b"$M>") or res[3]+6 != len(res) or res[-1] != calculateChecksum(res[:-1]):
			if res[0:3] != bytearray(b"$M>"):
				err = "Message header is invalid!"
			elif res[3]+6 != len(res):
				err = "Message length is invalid!"
			elif res[-1] != calculateChecksum(res[:-1]):
				err = f"Message checksum is invalid!\nReceived: {res[-1]} Expected: {calculateChecksum(res[:-1])}"
			data = []
		else:
			# Extract data from response
			data = res[5:-1]

		if DBG_REC:
			if err:
				print(err)
			print("Payload: ")
			for i in range(5, len(res)-1):
				print(f"{hex(res[i])}", end=" ")
			print()

		return data
