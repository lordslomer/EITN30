import json
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
MAX_CAPACITY = 382000

# performs a iperf3 udp test as a client with the options above
def run_test(load):
    client = iperf3.Client()
    client.server_hostname = SERVER_ADDR
    client.port = PORT
    client.protocol = PROTOCOL
    client.blksize = PACKET_SIZE
    client.duration = TEST_DURATION
    client.bandwidth = load
    return client.run()

# The interval step to take between loads
speed_step = (MAX_CAPACITY-LOWEST_TEST_SPEED)/((NBR_OF_TESTS*2)/3)

# Build the list of speeds to test 
loads = [int(LOWEST_TEST_SPEED + i * speed_step) for i in range(NBR_OF_TESTS)]

# Dict that stores the traffic intensity for each test
archive = {}

for load in loads:
    results = run_test(load)
    if results.error:
        print(results.error)
    else:
        rho = results.bps / MAX_CAPACITY
        print(f'Test completed for offered load {load} bps (ρ = {rho:.2f}):')
        print(f'  Took {results.seconds:.2f} seconds started at {results.time}')
        print(f'  Packet loss (%): {results.lost_percent}')
        print(f'  Jitter (ms): {results.jitter_ms:.4f}')
        print(f'  client bps: {results.bps:.2f}')
        print("")
        archive[results.time] = rho

# Save the archive dict into a file for plotting
if len(archive) == NBR_OF_TESTS:
    with open('results/iperf3_client_results.txt', 'w') as client_results: 
        client_results.write(json.dumps(archive))