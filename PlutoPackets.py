from telnetlib import Telnet

def calculateChecksum(data):
	checksum = 0
	for byte in bytearray(data)[3:]:
		checksum ^= byte
	return int.to_bytes(checksum, 1, 'little')

def createPacket(dir, cmd, data):
	header = [b"$M", bytes(dir, 'ascii'), int.to_bytes(len(data*2), 1, 'little'), int.to_bytes(cmd, 1, 'little')]

	payload = []
	for d in data:
		payload.append(int.to_bytes(d, 2, 'little'))

	packet = header + payload
	print(packet)
	packet += [calculateChecksum(packet)]


# header = [b"$M", b"<", int.to_bytes(2, 1, 'little'), int.to_bytes(217, 1, 'little')]


# packet = b""
# for h in header:
# 	packet += h
# for p in payload:
# 	packet += int.to_bytes(p, 2, 'little')

# packet += calculateChecksum(packet)
packet = createPacket('<', 217, [1])
print(packet)

# with Telnet('192.168.4.1', 23) as tn:
# 	tn.open('192.168.4.1', 23)
# 	# Send packet to host
# 	tn.write(packet)
# 	# Read response from host
# 	print(tn.read_all())