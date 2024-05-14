import json
import os
import iperf3

SERVER_ADDR = '10.0.0.1'
PORT = 12739
NBR_OF_TESTS = 24

# Create a iperf3 server that listens on addr and port above
server = iperf3.Server()
server.bind_address = SERVER_ADDR
server.port = PORT

# Dict that stores the practical throughput of the system for each test
archive = {}

# Perform and record the result of the next 24 tests
print("Waiting for the first test...")
for i in range(NBR_OF_TESTS):
    results = server.run()
    if results.error:
        print(results.error)
    else:
        server_load = results.json['end']['sum_received']['bits_per_second']/1000
        archive[results.time] = server_load
        print(f'Test {i+1} completed:')
        print(f'  Started at:       {results.time}')
        print(f'  Test duration:    {results.seconds:.2f} seconds')
        print(f'  Packet loss (%):  {results.lost_percent}')
        print(f'  Jitter (ms):      {results.jitter_ms:.4f}')
        print(f'  Server (Kbps):    {server_load:.2f}')
        print("")
        
# Save the archive dict into a file for plotting
if len(archive) == NBR_OF_TESTS:
    with open(os.path.join(os.path.dirname(__file__),'results/iperf3_server_results.txt'), 'w') as server_results: 
        server_results.write(json.dumps(archive))
