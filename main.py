from PID.poshold import PosHold
from position.optitrack import Optitrack


def main():
	estimator = Optitrack(hostname="192.168.4.2")
	posHold = PosHold(estimator)

	posHold.run(10)

if __name__ == "__main__":
	main()
