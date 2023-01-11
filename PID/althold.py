from simple_pid import PID
from position.arucoDetection import arucoDetection
import control
from time import time

class AltitudeHold:
    def __init__(self, dist, estimator=arucoDetection()):
        
        self.position = estimator
        while not self.position.setOrigin(1):
            print("Setting origin")
            pass
        self.drone = control.Pluto()
        self.distance = dist
        
        
    def setupPID(self, Kp=0.1, Ki=0.5, Kd=0.01, sample_time=0.01):
                

        self.pid = PID(Kp, Ki, Kd, setpoint=self.distance)
        self.pid.sample_time = sample_time
        

    
    def althold(self, duration):
        
        self.drone.arm()
        
        start = time()
        
        while time() < start + duration:
            pos = self.position.getPose(1)
            if len(pos)==0:
                break
            ori, (x, y, z) = pos
            output = self.pid(z)
            
            self.drone.rc(1500, 1500, 1000 + output, 1500)
        
        self.drone.disarm()
            
            
 



