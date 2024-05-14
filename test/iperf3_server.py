import json
import iperf3

SERVER_ADDR = '10.0.0.1'
PORT = 12739

server = iperf3.Server()
server.bind_address = SERVER_ADDR
server.port = PORT

archive = {}

while True:
    results = server.run()
    if results.error:
        print(results.error)
    else:
        print('Test completed:')
        print(f'  Took {results.seconds:.2f} seconds started at {results.time}')
        print(f'  Packet loss (%): {results.lost_percent}')
        print(f'  Jitter (ms): {results.jitter_ms:.4f}')
        server_load = results.json['end']['sum_received']['bits_per_second']/1000
        print(f'  server (Kbps): {server_load:.2f}')
        print("")
        archive[results.time] = server_load
        
        with open('iperf3_server_results.txt', 'w') as server_results: 
            server_results.write(json.dumps(archive))
