import socket
import time

# Set the server address and port
SERVER_ADDR = '10.0.0.1'
PACKET_SIZE = 1448
PORT = 12739

# Create a UDP socket
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind((SERVER_ADDR, PORT))
print(f"Server listening at {SERVER_ADDR}:{PORT}")

# Helper function to get time in micro seconds
def time_in_micro():
    return int(time.time() * 1000000)

# Helper function micro seconds -> seconds
def micro_to_sec(micro):
    return micro / 1000000


try:
    while True:
        # Receive packets
        message, client_addr = socket_server.recv(PACKET_SIZE) 
        timestamp = int.from_bytes(message[:8], 'big')
        rtt = time_in_micro() - timestamp

except KeyboardInterrupt:
    socket_server.close()