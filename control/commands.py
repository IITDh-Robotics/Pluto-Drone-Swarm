from control.connection import Connection
from control.packets import createPacket
from control.consts import *

class Pluto:
	def __init__(self, host="192.168.4.1", port=23):
		self.conn = Connection(host, port)
		self.conn.connect()

	def arm(self):
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [C, C, L, L, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, ARM])
		self.conn.send(packet)

	def disarm(self):
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [C, C, L, H, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, DISARM])
		self.conn.send(packet)

	def rc(self, roll, pitch, throttle, yaw):
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [roll, pitch, throttle, yaw, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, ARM])
		print(f"Sending roll:{roll}, pitch:{pitch}, throttle:{throttle}, yaw:{yaw}")
		self.conn.send(packet)

	def takeoff(self):
		packet = createPacket(MSG_IN, MSP_SET_COMMAND, [TAKE_OFF])
		self.conn.send(packet)

	def land(self):
		packet = createPacket(MSG_IN, MSP_SET_COMMAND, [LAND])
		self.conn.send(packet)

	def getAltitude(self):
		packet = createPacket(MSG_IN, MSP_ALTITUDE)
		self.conn.send(packet)
		data = self.conn.receive()
		# Returns Altitude, Vario
		return int.from_bytes(data[0:4], "little"), int.from_bytes(data[4:6], "little")

	def getAnalog(self):
		packet = createPacket(MSG_IN, MSP_ANALOG)
		self.conn.send(packet)
		data = self.conn.receive()
		# Returns Battery Voltage, mAH Drawn, Amperage
		return int.from_bytes(data[0:2], "little"), int.from_bytes(data[2:6], "little"), int.from_bytes(data[6:10], "little")
