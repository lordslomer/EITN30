import socket
import time
import json

SERVER_ADDR = '10.0.0.1'
PORT = 12739
PACKET_SIZE = 1448
TEST_DURATION = 10  # seconds
MAX_CAPACITY = 382000  # bits per second
LOWEST_TEST_SPEED = 2000  # bits per second
NUM_PACKETS = 100

def run_test(load):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER_ADDR, PORT)
    message = b'x' * PACKET_SIZE

    rtt_list = []
    sent_packets = 0

    start_time = time.time()
    while time.time() - start_time < TEST_DURATION:
        sent_time = time.time()
        sock.sendto(message, server_address)
        try:
            sock.settimeout(1)
            data, server = sock.recvfrom(PACKET_SIZE)
            recv_time = time.time()
            rtt = (recv_time - sent_time) * 1000  # Convert to milliseconds
            rtt_list.append(rtt)
        except socket.timeout:
            pass
        sent_packets += 1

    sock.close()
    return rtt_list, sent_packets

def calculate_rho(sent_packets, load):
    effective_load = sent_packets * PACKET_SIZE * 8 / TEST_DURATION  # bits per second
    rho = effective_load / MAX_CAPACITY
    return rho

def main():
    speed_step = (MAX_CAPACITY - LOWEST_TEST_SPEED) / 16
    loads = [int(LOWEST_TEST_SPEED + i * speed_step) for i in range(24)]

    archive = {}

    for load in loads:
        rtt_list, sent_packets = run_test(load)
        if rtt_list:
            avg_rtt = sum(rtt_list) / len(rtt_list)
        else:
            avg_rtt = float('inf')
        rho = calculate_rho(sent_packets, load)
        print(f'Test completed for offered load {load} bps (ρ = {rho:.2f}):')
        print(f'  Average RTT (ms): {avg_rtt:.2f}')
        archive[time.time()] = {'rho': rho, 'avg_rtt': avg_rtt}

    with open('udp_rtt_results.txt', 'w') as results_file:
        results_file.write(json.dumps(archive, indent=4))

if __name__ == '__main__':
    main()
