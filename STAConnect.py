# This script can be used to connect the pluto to a wireless network

from telnetlib import Telnet
from time import sleep

host, port = "192.168.4.1", 23
ssid, password = "control_lab", "12345678"

tn = Telnet(host, port)

print("Changing connection mode to 3...")
tn.write("+++AT MODE 3\n".encode("ascii"))
print(tn.read_some().decode('ascii'))
print(f"Connecting to {ssid}...")
tn.write(f"+++AT STA {ssid} {password}\n".encode("ascii"))
print(tn.read_some().decode('ascii'))
sleep(5)
print("Connected!")
tn.write("+++AT SHOWIP\n".encode("ascii"))
print(tn.read_some().decode('ascii'))

tn.close()
