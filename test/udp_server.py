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

# Helper function us -> s
def micro_to_sec(micro):
    return micro / 1000000

# List of round trip times
RTTs =[]
try:
    while True:
        # Receive packet 
        message, client_addr = socket_server.recvfrom(PACKET_SIZE) 
        header = message[:8]

        # If end of test packet, calc avg_rtt and send it back
        if header == b"E" * 8:
            # calc avg_rtt
            avg_rtt = int(sum(RTTs)/len(RTTs))

            # create payload out of avg_rtt
            result_payload = avg_rtt.to_bytes(4, 'big')

            # Send avg_rtt as test result
            socket_server.sendto(result_payload, client_addr)
            print(f"Test done with an avg latency: {avg_rtt/1000:.2f} ms\n")
            RTTs = []
        else:
            # otherwise, inc RTT list with the packet's rtt. 
            timestamp = int.from_bytes(header, 'big')
            RTTs.append(time_in_micro() - timestamp)

except KeyboardInterrupt:
    socket_server.close()