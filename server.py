import socket
import time

# Set the server address and port
socket_addr = '10.0.0.1'
socket_port = 12739

# Create a UDP socket
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind((socket_addr, socket_port))
print(f"Server listening at {socket_addr}:{socket_port}")


def time_in_micro():
    return int(time.time() * 1000000)

def micro_to_sec(micro):
    return micro / 1000000
    

packet_size = 1024
total_packets = 5
service_times = []
packge_recv = [0 for _ in range(total_packets)]
end_payload = b"X"*packet_size

def close():
    socket_server.close()
    nbr_packets_recv = sum(packge_recv)
    print(f"Server shutdown. Total packets received: {nbr_packets_recv} / {total_packets} - {(nbr_packets_recv/total_packets)*100:.2f}%")
    service_time_avg = sum(service_times)/len(service_times)
    print(micro_to_sec(service_time_avg))

try:
    while True:
        # Receive packets
        message, client_addr = socket_server.recvfrom(packet_size) 

        if message == end_payload:
            close()
            break
        else:
            timestamp = int.from_bytes(message[:8], 'big')
            service_times.append(time_in_micro() - timestamp)
            index = int.from_bytes(message[8:], 'big')
            packge_recv[index] = 1

except KeyboardInterrupt:
    close()
