import time
from commands import Pluto


def main():
    pluto = Pluto()

    #pluto.arm()
    pluto.get_alti()
    #pluto.disarm()
	#print("Taking Off")
	#pluto.takeoff()
	#time.sleep(2)
	#print("Increasing Throttle")
	#pluto.rc(1500, 1500, 2000, 1500)
	#time.sleep(2)
	#print("Landing")
	#pluto.land()
    

if __name__ == '__main__':
	main()
