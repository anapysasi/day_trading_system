import socket
import sys

HOST, PORT = "localhost", 9995
data = "5"

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = []
    for _ in range(100):
        received.append(str(sock.recv(1024), "utf-8"))
        # act on the data
        # feed relevant data into model

print("Sent:     {}".format(data))
print("Received: {}".format(received[0]))
print("Received: {}".format(received[1]))
print("Received: {}".format(received))