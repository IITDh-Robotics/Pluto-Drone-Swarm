from control.connection import Connection
from control.packets import createPacket
from control.consts import *
from time import sleep

class Pluto:
	'''
	An instance of this class can be used to interact with the drone. A connection is established with the drone when an instance of this class is created.

	Optionally the host and port of the drone can be specified.
	'''
	def __init__(self, host="192.168.4.1", port=23):
		self.conn = Connection(host, port)
		self.conn.connect()

	def __del__(self):
		self.disarm()

	def arm(self):
		'''
		Arms the drone.
		'''
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [C, C, L, L, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, ARM])
		self.conn.send(packet)
		sleep(1)

	def disarm(self):
		'''
		Disarms the drone.
		'''
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [C, C, L, H, YAW_HEAD_FREE, DEV_MODE_OFF, ALT_HOLD_OFF, DISARM])
		self.conn.send(packet)
		sleep(1)

	def rc(self, roll, pitch, throttle, yaw, althold=False):
		'''
		This function sends the roll, pitch, throttle and yaw values to the drone as a RC message.
		'''
		althold_mode = ALT_HOLD_ON if althold else ALT_HOLD_OFF
		packet = createPacket(MSG_IN, MSP_SET_RAW_RC, [roll, pitch, throttle, yaw, YAW_HEAD_FREE, DEV_MODE_OFF, althold_mode, ARM])
		# print(f"Sending roll:{roll}, pitch:{pitch}, throttle:{throttle}, yaw:{yaw}")
		self.conn.send(packet)

	def takeoff(self):
		'''
		Sends instruction for taking off.
		'''
		packet = createPacket(MSG_IN, MSP_SET_COMMAND, [TAKE_OFF])
		self.conn.send(packet)

	def land(self):
		'''
		Sends instruction for landing.
		'''
		packet = createPacket(MSG_IN, MSP_SET_COMMAND, [LAND])
		self.conn.send(packet)

	def getAltitude(self):
		'''
		Returns the altitude and vario of the drone.
		'''
		packet = createPacket(MSG_IN, MSP_ALTITUDE)
		self.conn.send(packet)
		data = self.conn.receive()
		# Returns Altitude, Vario
		return int.from_bytes(data[0:4], "little"), int.from_bytes(data[4:6], "little")

	def getAnalog(self):
		'''
		Returns the battery voltage, mAH drawn, RSSI and amperage of the drone.
		'''
		packet = createPacket(MSG_IN, MSP_ANALOG)
		self.conn.send(packet)
		data = self.conn.receive()
		sleep(0.5)
		# return 0.1*int.from_bytes(data[0:1], "little"), int.from_bytes(data[2:4], "little"), 0.01*int.from_bytes(data[4:6], "little"), int.from_bytes(data[6:8], "little")
		return 0.1*int.from_bytes(data[0:1], "little")
