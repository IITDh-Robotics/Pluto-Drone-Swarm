import time
from commands import Pluto
from math import ceil
pluto = Pluto()


def main():

	pluto = Pluto()

	while True:
		pluto.getAltitude()
		time.sleep(5)    

if __name__ == '__main__':
	main()

