from control.consts import *

'''
Functions for handling MSP packets.
'''

def calculateChecksum(packet):
	'''
	This function returns the checksum of a packet. A byte array of the packet should be passed as a parameter.
	'''

	checksum = 0
	for byte in bytearray(packet)[3:]:
		checksum ^= byte
	return int.to_bytes(checksum, 1, 'little')

def createPacket(dir, cmd, data = []):
	'''
	Creates a packet to be sent to the drone. Returns a properly structured packet which can be sent to the drone.
	
	:param dir: The direction in which your message goes.
	:param cmd: Command code. 
	:param data: Payload data sent to the drone.
	'''

	header = b"$M" 										# Msg Header = $M
	header += dir										# Msg Direction = < or >
	header += int.to_bytes(len(data)*2, 1, 'little')	# Msg Length = 2 * Data Length
	# print(cmd)
	header += int.to_bytes(cmd, 1, 'little')			# Msg Command
	#print(header)
	payload = b""
	for d in data:
		payload += int.to_bytes(d, 2, 'little')

	packet = header + payload
	packet += calculateChecksum(packet)

	return packet
