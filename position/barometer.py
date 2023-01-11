import time
from math import ceil
class Barometer():
    def __init__(self, pluto) -> None:
        self.pluto = pluto
        self.altiSubtract = 0
        pass

    def setOrigin(self,PlutoId):
        r = 0
        heights = 0
        while r < 10:
            alti_packet = self.pluto.get_alti()
            if len(alti_packet) > 5:
                height = alti_packet[5]  #5th byte appears to be changing like height
                heights += height
                r += 1
        avgHeight = ceil(heights/10)
        self.altiSubtract = avgHeight

    def getPose(self, PlutoId):
        alti_packet = self.pluto.get_alti()

        return [], [-1, -1, alti_packet[5] - self.altiSubtract]#height