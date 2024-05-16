import os
import pickle
import iperf3

SERVER_ADDR = '10.0.0.1'
PORT = 12739

# Default iperf3 udp test params
PACKET_SIZE = 1448
TEST_DURATION = 10
PROTOCOL = 'udp'

# Help determine the list of speeds/loads to be tested
LOWEST_TEST_SPEED = 2000
NBR_OF_TESTS = 24
NONE_OVERLOADED_RATIO = 2/3
MAX_CAPACITY = 410000

# performs a iperf3 udp test as a client with the options above
def run_throughput(load):
    client = iperf3.Client()
    client.server_hostname = SERVER_ADDR
    client.port = PORT
    client.protocol = PROTOCOL
    client.blksize = PACKET_SIZE
    client.duration = TEST_DURATION
    client.bandwidth = load
    return client.run()

# The interval step to take between loads
speed_step = (MAX_CAPACITY-LOWEST_TEST_SPEED)/(NBR_OF_TESTS * NONE_OVERLOADED_RATIO)

pairs = []
print("Starting test...")
for test in range(NBR_OF_TESTS):
    load = int(LOWEST_TEST_SPEED + test * speed_step)
    results = run_throughput(load)

    if results.error:
        print(results.error)
    else:
        rho = results.bps / MAX_CAPACITY
        server_load = results.json['end']['sum_received']['bits_per_second']/1000
        pairs.append((server_load,rho))
        
        print(f'Test {test+1}/{NBR_OF_TESTS} for load {load/1000:.2f} Kbps (ρ = {rho:.2f}):')
        print(f'  Started at:       {results.time}')
        print(f'  Test duration:    {results.seconds:.2f} seconds')
        print(f'  Packet loss (%):  {results.lost_percent}')
        print(f'  Jitter (ms):      {results.jitter_ms:.4f}')
        print(f'  Client (Kbps):    {results.kbps:.2f}')
        print("")

# Save paris to file
with open(os.path.join(os.path.dirname(__file__),'results/throughput-rho.txt'), 'wb') as f:
    pickle.dump(pairs,f)

