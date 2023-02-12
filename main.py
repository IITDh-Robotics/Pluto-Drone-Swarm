from time import sleep, time
from control.poshold import PosHold
from position.arucoDetection import arucoDetection
from position.optitrack import Optitrack

def detect():
	estimator = arucoDetection(arucoMarkerSize=0.02)
	while not estimator.setOrigin(1):
		pass
	while True:
		start = time()
		print(estimator.getPose(1))
		print(1/(time() - start))

def hover():
	# estimator = Optitrack(hostname="10.250.60.47")
	estimator = arucoDetection(arucoMarkerSize=0.04)
	posHold = PosHold(estimator, ids=[1, 0], hosts=["192.168.143.54", "192.168.143.165"])

	posHold.PIDControls[0].drone.arm()
	posHold.PIDControls[1].drone.arm()
	posHold.hold([[0,0,0.5], [0,0,0.5]], 10)
	# posHold.hold([[0.5,0,0.5]], 10)
	# posHold.hold([2,1,1], 5)
	# posHold.hold([0,1,1], 5)
	# posHold.hold([0,0,1], 5)
	posHold.PIDControls[0].drone.land()
	posHold.PIDControls[1].drone.land()
	sleep(1)
	posHold.PIDControls[0].drone.disarm()
	posHold.PIDControls[1].drone.disarm()

def single():
	estimator = arucoDetection(arucoMarkerSize=0.04)
	posHold = PosHold(estimator, ids=[0], hosts=[ "192.168.143.165"])

	posHold.PIDControls[0].drone.arm()
	posHold.hold([[0,0,0.5]], 10)
	# posHold.hold([[0.5,0,0.5]], 10)
	# posHold.hold([2,1,1], 5)
	# posHold.hold([0,1,1], 5)
	# posHold.hold([0,0,1], 5)
	posHold.PIDControls[0].drone.land()
	sleep(1)
	posHold.PIDControls[0].drone.disarm()


if __name__ == "__main__":
	# hover()
	# single()
	detect()
