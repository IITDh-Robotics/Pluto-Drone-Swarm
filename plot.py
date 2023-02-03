import json
import sys
from matplotlib import pyplot as plt
import numpy as np


def plot(file, altitute=False):
	hist = json.load(open(file))

	plt.title(hist["pid"])
	if not altitute:
		for axis in range(2):
			plt.hlines(np.array(hist["setpoint"][0][axis]), 0, len(hist["pos"]), colors="k")
			plt.plot(np.array(hist["pos"])[:,axis])
		plt.legend(["x setpoint","x", "y setpoint", "y"])
		plt.savefig("".join(sys.argv[1].split(".")[:-1]))
	else:
		axis = 2
		plt.hlines(np.array(hist["setpoint"][0][axis]), 0, len(hist["pos"]), colors="k")
		plt.plot(np.array(hist["pos"])[:,axis])
		plt.plot(np.array(hist["control"])[:,axis]/500)
		plt.legend(["setpoint","altitude", "control"])
		plt.savefig("".join(sys.argv[1].split(".")[:-1])+"alt")
	plt.show()

if __name__ == "__main__":
	if len(sys.argv) == 2:
		plot(sys.argv[1])
	else:
		plot(sys.argv[1], True)