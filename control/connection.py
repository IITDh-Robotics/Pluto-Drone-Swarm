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
		#print('sending from send():', data)
		#self.tn.read_eager()

	def disconnect(self):
		self.tn.close()
		print("Disconnected from pluto at " + self.host + ":" + self.port + ".")

	def receive(self):
		print('about to read...')
		dat1 = self.tn.read_some()
		
		return dat1
