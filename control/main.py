import time
from commands import Pluto
from math import ceil
pluto = Pluto()

def height_calib():
	r = 0
	heights = 0
	time.sleep(20)
	while r < 10:
		alti_packet = pluto.get_alti()
		if len(alti_packet) > 5:
			height = alti_packet[5]  #5th byte appears to be changing like height
			heights += height
			r += 1
	avgHeight = ceil(heights/10)
	return avgHeight


def main():
	
	height_cal = height_calib()
	print(height_cal)
	while True:
		alti_packet = pluto.get_alti()
		# r = 0
		# heights = 0
		# while r < 10:
			
		# 	if len(alti_packet) > 5:
		# 		height = alti_packet[5]  #5th byte appears to be changing like height
		# 		heights += height
		# 		r += 1
		# avgHeight = ceil(height/10)

		print('alti_Packet', alti_packet)
		time.sleep(1)
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

