from connection import Connection
from packets import createPacket
from consts import *
from time import sleep

class Pluto:
	def __init__(self):
		self.conn = Connection()
		self.conn.connect()

	def arm(self):
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [C, C, L, L, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, ARM])
		print('about to send arm:')
		self.conn.send(packet)
		print('sent arm:', packet)

	def takeoff(self):
		packet = createPacket(MSG_IN, MSP_SET_COMMAND, [TAKE_OFF])
		print(MSP_SET_COMMAND)
		self.conn.send(packet)

	def rc(self, roll, pitch, throttle, yaw):
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [roll, pitch, throttle, yaw, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, ARM])

	def land(self):
		packet = createPacket(MSG_IN, MSP_SET_COMMAND, [LAND])
		self.conn.send(packet)

	def disarm(self):
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [C, C, H, L, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, DISARM])
		self.conn.send(packet)
		print('sent disarm:', packet)

	def get_alti(self):
		packet = createPacket(MSG_IN, MSP_ALTITUDE)
		self.conn.send(packet)
		
		print('sent alti req:', packet)
		to_be_returned = []

		for byte in bytearray(self.conn.receive()):
			to_be_returned.append(byte)
		

		return to_be_returned
