from simple_pid import PID
from position.arucoDetection import arucoDetection
import control
from time import time

# class AltitudeHold:
#     def __init__():
        
# Create a position object

position = arucoDetection("http://10.196.4.192:8080/shot.jpg")
position.setOrigin(1)

pos, ori = position.getPose(1)
x, y, z = pos[0], pos[1], pos[2]

# Parameter Tuning

Kp = 0.1
Kd = 0.5
Ki = 0.01



pid = PID(Kp, Ki, Kd, setpoint=0)
pid.sample_time = 0.01

# Set the required height of the drone

pid.setpoint = 0.5 # in meters

drone = control.Pluto()

drone.arm()

start = time()

while time() < start + 60:
    pos, ori = position.getPose(1)
    x, y, z = pos[0], pos[1], pos[2]
    output = pid(z)
    
    drone.rc(1500, 1500, 1000 + output, 1500)
    
drone.disarm()



