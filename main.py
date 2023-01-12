from PID.althold import AltitudeHold


def main():
	altHold = AltitudeHold(0)

	altHold.setupPID()

	altHold.althold(30)

if __name__ == "__main__":
	main()