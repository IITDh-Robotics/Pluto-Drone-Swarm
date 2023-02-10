import socket
import subprocess
import cv2
import numpy as np

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    ffmpegCmd = ['ffmpeg', '-i', '-', '-f', 'rawvideo', '-vcodec', 'bmp', '-vf', 'fps=5', '-']
    ffmpeg = subprocess.Popen(ffmpegCmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE)

    while True:
        # Reading data from the socket
        data = connection.read(1024)
        if not data:
            break

        # Writing to ffmpeg
        ffmpeg.stdin.write(data)

        # Converting to OpenCv image
        fileSizeBytes = ffmpeg.stdout.read(6)
        fileSize = 0
        for i in range(4):
            fileSize += fileSizeBytes[i + 2] * 256 ** i
        bmpData = fileSizeBytes + ffmpeg.stdout.read(fileSize - 6)
        image = cv2.imdecode(np.fromstring(bmpData, dtype = np.uint8), 1)
        cv2.imshow(image)
        
finally:
    connection.close()
    server_socket.close()
    ffmpeg.terminate()
    cv2.waitKey(0)
    cv2.destroyAllWindows()