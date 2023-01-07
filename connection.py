import telnetlib


class Connection:
	def __init__(self, host="192.168.4.1", port="23"):
		self.host = host
		self.port = port

	def connect(self):
		print("Connecting to pluto at " + self.host + ":" + self.port + "...")
		try:
			self.tn = telnetlib.Telnet(self.host, self.port)
			print("Connection successful!")
		except:
			print("Connection failed!")
		
	def send(self, data):
		self.tn.write(data)

	def disconnect(self):
		self.tn.close()
		print("Disconnected from pluto at " + self.host + ":" + self.port + ".")