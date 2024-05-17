import os
import pickle
import matplotlib.pyplot as plt
import socket
import time

# Server address and port
SERVER_ADDR = '10.0.0.1'
PACKET_SIZE = 1448       
TEST_DURATION = 10
PORT = 12739

# Values needed to determine the list of speeds/loads to be tested
LOWEST_TEST_SPEED = 2000
NBR_OF_TESTS = 24
NONE_OVERLOADED_RATIO = 2/3
MAX_CAPACITY = 410000

# Create a UDP socket
socket_con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_con.settimeout(30)

# Helper function to get time in micro seconds
def time_in_micro():
    return int(time.time() * 1000000)

def run_latency_test(load):
    # Calculate the time interval between packets to maintain the target_speed
    time_per_packet = (PACKET_SIZE * 8) / load

    # Track cumulative ideal send time
    start_time = time.time()
    cumulative_ideal_time = start_time

    # While time is within test duration
    while (time.time() - start_time) <= TEST_DURATION:
        # Construct and send the payload
        payload =  time_in_micro().to_bytes(8,'big') + b"X" * (PACKET_SIZE - 8)
        socket_con.sendto(payload, (SERVER_ADDR, PORT))

        # Update the ideal time
        cumulative_ideal_time += time_per_packet
        sleep_time = cumulative_ideal_time - time.time()

        # Sleep for ideal sleep_time to maintain target_speed
        if sleep_time > 0: 
            time.sleep(sleep_time)
    
    # Send end_of_test packet
    end_payload = b"E" * 8 + b"X" * (PACKET_SIZE - 8)
    socket_con.sendto(end_payload, (SERVER_ADDR, PORT))

    # Recive test results
    avg_rtt = int.from_bytes(socket_con.recv(4), 'big')
    return avg_rtt

# The interval step to take between testing loads
speed_step = (MAX_CAPACITY-LOWEST_TEST_SPEED)/(NBR_OF_TESTS * NONE_OVERLOADED_RATIO)

# List for the resulting loads
pairs = []
for test in range(NBR_OF_TESTS):
    # calc the load to be tested
    load = int(LOWEST_TEST_SPEED + test * speed_step)
    rho = load/MAX_CAPACITY
    print(f"Begin Test for load {load/1000:.2f} Kbps (ρ = {rho:.2f})")

    # run the test
    avg_rtt = run_latency_test(load)

    # add the test result to list
    pairs.append((avg_rtt/1000,rho))
    print(f"Test done with an avg latency: {avg_rtt/1000:.2f} ms\n")

# Save results to file
with open(os.path.join(os.path.dirname(__file__),'results/latency-rho.txt'), 'wb') as f:
    pickle.dump(pairs,f)

socket_con.close()


