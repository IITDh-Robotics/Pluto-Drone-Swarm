from time import sleep, time
from control.poshold import PosHold
from position.arucoDetection import arucoDetection
from position.optitrack import Optitrack

def detect():
	estimator = arucoDetection()
	# while not estimator.setOrigin(1):
	# 	pass
	while True:
		start = time()
		print(estimator.getPose(1))
		print(1/(time() - start))

def hover():
	# estimator = Optitrack(hostname="10.250.60.47")
	estimator = arucoDetection(arucoMarkerSize=0.04)
	posHold = PosHold(estimator, host="10.250.60.89")

	posHold.drone.arm()
	posHold.hold([0,0,1], 5)
	posHold.hold([2,0,1], 5)
	posHold.hold([2,1,1], 5)
	posHold.hold([0,1,1], 5)
	posHold.hold([0,0,1], 5)
	posHold.drone.land()
	sleep(1)
	posHold.drone.disarm()


if __name__ == "__main__":
	# hover()
	detect()
