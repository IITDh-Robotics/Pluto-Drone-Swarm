from telnetlib import Telnet


def calculateChecksum(data):
	checksum = 0
	for byte in bytearray(data)[3:]:
		checksum ^= byte
	return int.to_bytes(checksum, 1, 'little')

def createPacket(dir, cmd, data):
	header = b"$M" 										# Msg Header = $M
	header += bytes(dir, 'ascii')						# Msg Direction = < or >
	header += int.to_bytes(len(data*2), 1, 'little')	# Msg Length = 2 * Data Length
	header += int.to_bytes(cmd, 1, 'little')			# Msg Command

	payload = b""
	for d in data:
		payload += int.to_bytes(d, 2, 'little')

	packet = header + payload
	packet += calculateChecksum(packet)

	return packet