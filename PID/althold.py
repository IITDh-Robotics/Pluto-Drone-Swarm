from simple_pid import PID
from position.arucoDetection import arucoDetection
from control.commands import Pluto
from time import time, sleep

class AltitudeHold:
    def __init__(self, dist, id=0, estimator=arucoDetection()):
        self.id = id
        self.position = estimator
        while not self.position.setOrigin(self.id):
            print("Setting origin")
            pass
        print("Origin Set!")
        self.drone = Pluto()
        self.distance = dist
        
        
    def setupPID(self, Kp=-2000, Ki=0.5, Kd=0.01, sample_time=0.01):
        self.pid = PID(Kp, Ki, Kd, setpoint=self.distance)
        self.pid.sample_time = sample_time
        self.pid.output_limits = (0,1000)
        print("PID setup done")
        

    
    def althold(self, duration):
        
        self.drone.arm()

        sleep(2)
        
        start = time()

        count = 0
        
        while time() < start + duration:
            pos = self.position.getPose(self.id)
            if len(pos)==0:
                count += 1
            else:
                print("------------Marker detected------------")
                count = 0
                ori, (x, y, z) = pos
                print("z = ", z)
                output = int(self.pid(z))
                print("PID output: ", output)
                self.drone.rc(1500+10, 1500+20, 1000 + output, 1500)\
            
            if count == 40:
                print("Count == ", count)
                break

            sleep(0.1)
        
        self.drone.disarm()
        print("Drone disarmed")
            
            
 



