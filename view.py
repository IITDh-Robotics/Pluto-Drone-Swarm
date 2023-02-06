from socket import socket
import cv2


if __name__ == "__main__":
	# Create a TCP/IP socket
	sock = socket()
	sock.bind(("localhost", 8000))
	sock.listen(1)

	while True:
		data = sock.recv(1024)
		cv2.imshow("frame", data)
		cv2.waitKey(1)