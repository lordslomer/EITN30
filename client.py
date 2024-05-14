import socket
import time

# Server address and port
socket_addr = '10.0.0.1'
socket_port = 12739

# Create a UDP socket
socket_con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_con.settimeout(5)

# Target data rate in bytes per second (300 KB/s)
target_rate_bps = 100 * 1024  # 300 KBps in bytes per second
packet_size = 1024

# Calculate the time interval between packets to maintain the target rate
time_per_packet = 1

# Total packets to send
total_packets = 5

# Track cumulative ideal send time
cumulative_ideal_time = time.time()

def time_in_micro():
    return int(time.time() * 1000000)

end_payload = b"X"*packet_size

try:
    start_time = time.time()
    
    for i in range(total_packets):
        # Construct the payload
        payload =  time_in_micro().to_bytes(8,'big') + i.to_bytes(packet_size-8, 'big')
        socket_con.sendto(payload, (socket_addr, socket_port))
        
        # Update the ideal time
        cumulative_ideal_time += time_per_packet
        current_time = time.time()
        sleep_time = cumulative_ideal_time - current_time

        if sleep_time > 0:
            time.sleep(sleep_time)

    
    socket_con.sendto(end_payload, (socket_addr, socket_port))
    end_time = time.time()
    
    # Calculate the duration and the data rate
    duration = end_time - start_time
    total_bytes_sent = total_packets * packet_size
    byterate = total_bytes_sent / duration

    # Print results
    print(f"Duration: {duration:.2f} seconds")
    print(f"Total bytes sent: {total_bytes_sent}")
    print(f"Data rate: {byterate / 1024:.2f} KB/s")
    print(f"Total packets sent: {total_packets}")
    print(f"Packets per second: {total_packets / duration:.2f}")
    print(f"Time per packet: {time_per_packet}")

except socket.timeout:
    print("Request timed out.")
finally:
    socket_con.close()
