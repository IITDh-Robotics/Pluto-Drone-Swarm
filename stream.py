from socket import socket
import picamera

if __name__ == "__main__":
	# Create a TCP/IP socket
	sock = socket()
	sock.connect(("192.168.4.2", 8000))

	camera = picamera.PiCamera()
	camera.resolution = (1280, 720)
	camera.framerate = 60
	camera.start_recording(sock, format="bgr")
