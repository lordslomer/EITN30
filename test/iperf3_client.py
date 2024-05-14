import json
import iperf3

SERVER_ADDR = '10.0.0.1'
PORT = 12739
PACKET_SIZE = 1448
TEST_DURATION = 10
PROTOCOL = 'udp'
MAX_CAPACITY = 382000
LOWEST_TEST_SPEED = 2000

def run_test(load):
    client = iperf3.Client()
    client.server_hostname = SERVER_ADDR
    client.port = PORT
    client.protocol = PROTOCOL
    client.blksize = PACKET_SIZE
    client.duration = TEST_DURATION
    client.bandwidth = load
    return client.run()

speed_step = (MAX_CAPACITY-LOWEST_TEST_SPEED)/16
loads = [int(LOWEST_TEST_SPEED + i * speed_step) for i in range(24)]

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
        
with open('iperf3_client_results.txt', 'w') as client_results: 
     client_results.write(json.dumps(archive))