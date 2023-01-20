from time import sleep
from PID.althold import AltitudeHold
from control.commands import Pluto


def main():
	pluto = Pluto("10.250.60.87")

	# while True:
	# 	alt, _, _ = pluto.getAnalog()
	# 	print(alt)
	# 	sleep(1)

	pluto.arm()
	sleep(1)
	pluto.rc(1500, 1500, 1500, 1500)
	sleep(2)
	pluto.disarm()

if __name__ == "__main__":
	main()