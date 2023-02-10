import numpy as np
import motioncapture

class Optitrack():
    def __init__(self, type="optitrack", hostname="192.168.4.2") -> None:
        self.mc = motioncapture.connect(type, {"hostname": hostname})
        self.origin = (0, 0, 0)

    def setOrigin(self, _):
        self.mc.waitForNextFrame()
        self.origin = np.mean(self.mc.pointCloud, axis=0)
        return True

    def getPose(self, _):
        self.mc.waitForNextFrame()
        pos = np.mean(self.mc.pointCloud, axis=0)

        return [], pos-self.origin