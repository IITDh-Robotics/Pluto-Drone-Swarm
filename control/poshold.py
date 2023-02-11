from glob import glob
import json
import math
from time import sleep, time

from plot import plot
from control.commands import Pluto
from simple_pid import PID

class PosHold:
	'''
	An instance of this class can be used to hold the drone at the specified position (passed as a parameter). PID control is used which is implemented using the simple_pid package.

	:param estimator: An instance of the posision estimator class. 
	:param pos: Position to be held.
	:param host: IP Address of the drone.
	'''
	def __init__(self, estimator, pos=[0,0,1], host="192.168.4.1"):
		self.record = False
		self.estimator = estimator
		if self.record:
			self.hist = {"pos": [], "control": [], "setpoint": []}

		# Set origin
		while not self.estimator.setOrigin(1):
			print("Setting origin")
		print("Origin Set!")
		self.drone = Pluto(host)
		self.pos = pos

		# Setup PID controllers
		kp, ki, kd = 105, 3, 60		# 80, 5, 0.1
		self.pidx = PID(kp, ki, kd, setpoint=self.pos[0])
		self.pidy = PID(kp, ki, kd, setpoint=self.pos[1])
		# self.pidz = PID(180, 20, 55, setpoint=self.pos[2])
		self.pidz = PID(500, 50, 55, setpoint=self.pos[2])

		if self.record:
			self.hist["pid"] = {"kp": kp, "ki": ki, "kd": kd}

		# Set PID controller output limits
		self.pidx.output_limits = (-500, 500)
		self.pidy.output_limits = (-500, 500)
		# self.pidz.output_limits = (-700, 300)
		self.pidz.output_limits = (-500, 500)

		# Set PID controller sample time
		herz = 15
		self.pidx.sample_time = 1/herz
		self.pidy.sample_time = 1/herz
		self.pidz.sample_time = 1/herz

	def __del__(self):
		if self.record:
			kp, ki, kd = self.hist["pid"]["kp"], self.hist["pid"]["ki"], self.hist["pid"]["kd"]
			idx = len(glob(f"tests/hist-{kp}-{ki}-{kd}_*.json"))
			json.dump(self.hist, open(f"tests/hist-{kp}-{ki}-{kd}_{idx}.json", "w"))

	def hold(self, pos=[0,0,1], duration=10):
		'''
		:param pos: The 3D coordinates at which the drone must be held.
		:param duration: The duration in seconds for which the position must be held.
		'''
		self.pos = pos
		if self.record:
			self.hist["setpoint"].append(self.pos)

		# Update setpoints
		self.pidx.setpoint = self.pos[0]
		self.pidy.setpoint = self.pos[1]
		self.pidz.setpoint = self.pos[2]

		start = time()
		while time() < start + duration:
			ori, (x, y, z) = self.estimator.getPose(1)
			if self.record:
				self.hist["pos"].append((float(x), float(y), float(z)))

			# Error handling
			if z > 3:
				break

			if math.isnan(x) or math.isnan(y) or math.isnan(z):
				self.drone.rc(1500, 1500, 1500, 1500, althold=True)
				continue
	
			# if (abs(self.pos[2] - z) < 0.01):
			# 	self.pidx.set_auto_mode(False, last_output=0)
			# 	print("---------------------------OFF!---------------------------------")

			# PID controller
			roll = self.pidx(x)
			pitch = self.pidy(y)
			throttle = self.pidz(z)
			if self.record:
				self.hist["control"].append((int(roll), int(pitch), int(throttle)))

			# Send commands to drone
			self.drone.rc(1500 + int(roll), 1500 + int(pitch), 1500 + int(throttle), 1500, althold=True)