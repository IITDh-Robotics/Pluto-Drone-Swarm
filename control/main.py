import time
from control.commands import Pluto
from math import ceil
pluto = Pluto()

def height_calib():
	r = 0
	heights = 0
	time.sleep(20)
	while r < 10:
		alti_packet = pluto.getAltitude()
		if len(alti_packet) > 5:
			height = alti_packet[5]  #5th byte appears to be changing like height
			heights += height
			r += 1
	avgHeight = ceil(heights/10)
	return avgHeight


def main():
	
	# height_cal = height_calib()
	# print(height_cal)
	# while True:
	# 	alti_packet = pluto.getAltitude()
	# 	# r = 0
	# 	# heights = 0
	# 	# while r < 10:
			
	# 	# 	if len(alti_packet) > 5:
	# 	# 		height = alti_packet[5]  #5th byte appears to be changing like height
	# 	# 		heights += height
	# 	# 		r += 1
	# 	# avgHeight = ceil(height/10)

	# 	print(alti_packet[5], alti_packet[5] - height_cal)
	# 	time.sleep(1)

	pluto = Pluto()

	while True:
		pluto.getAltitude()
		time.sleep(5)    

if __name__ == '__main__':
	main()

