from time import sleep, time
from control.poshold import PosHold
from position import arucoDetection
# from position.optitrack import Optitrack


def hover():
	# estimator = Optitrack(hostname="10.250.60.47")
	estimator = arucoDetection()
	posHold = PosHold(estimator, host="10.250.60.90")

	posHold.drone.arm()
	posHold.hold([0,0,1], 15)
	# posHold.hold([2,0,1], 5)
	# posHold.hold([2,1,1], 5)
	# posHold.hold([0,1,1], 5)
	# posHold.hold([0,0,1], 5)
	posHold.drone.land()
	sleep(2)
	posHold.drone.disarm()


if __name__ == "__main__":
	hover()
