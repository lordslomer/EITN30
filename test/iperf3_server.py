import iperf3

SERVER_ADDR = '10.0.0.1'
PORT = 12739

# Create a iperf3 server that listens on addr and port above
server = iperf3.Server()
server.bind_address = SERVER_ADDR
server.port = PORT

print("Waiting for the first test...")

while True:
    results = server.run()
    if results.error:
        print(results.error)
    else:
        server_load = results.json['end']['sum_received']['bits_per_second']/1000
        print(f'Test completed:')
        print(f'  Started at:       {results.time}')
        print(f'  Test duration:    {results.seconds:.2f} seconds')
        print(f'  Packet loss (%):  {results.lost_percent}')
        print(f'  Jitter (ms):      {results.jitter_ms:.4f}')
        print(f'  Server (Kbps):    {server_load:.2f}')
        print("")
        
