from PID.althold import AltitudeHold


def main():
	altHold = AltitudeHold(0.20)

	altHold.setupPID()

	altHold.althold(10)

if __name__ == "__main__":
	main()