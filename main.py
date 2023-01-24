from time import time
from PID.poshold import PosHold
from position.optitrack import Optitrack


def hover():
	estimator = Optitrack(hostname="10.250.60.47")
	posHold = PosHold(estimator, host="10.250.60.87")

	posHold.run(30)


if __name__ == "__main__":
	hover()
