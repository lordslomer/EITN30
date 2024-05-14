import json 
import matplotlib.pyplot as plt

# Read client result data
with open('iperf3_client_results.txt') as f: 
    client_dict = dict(json.loads(f.read()))  

# Read server result data
with open('iperf3_server_results.txt') as f: 
    server_dict = dict(json.loads(f.read()) )

if server_dict.keys() == client_dict.keys():
  # Pair up values from the two dicts using the timestamps as keys
  throughput, rho = zip(*[(server_dict[key], client_dict[key]) for key in server_dict.keys()])

  plt.figure(figsize=(10, 6))
  plt.plot(rho, throughput, marker='o', linestyle='-', color='b')
  plt.xlabel('Traffic Intensity (ρ)')
  plt.ylabel('Throughput (bps)')
  plt.savefig("throughput-rho.pdf")
  plt.title('Throughput vs. Traffic Intensity (ρ)')
  plt.grid(True)
  plt.savefig('throughput-rho.pdf')
else: 
  print("Sry, timestamps don't match on client and server results!")