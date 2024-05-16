# EITN30 - Internet Inuti

## Start the network
If you cannot execute *run.sh*, make the bash script execuatble: 
```
chmod +x run.sh
```

Start the base station:
```bash
./run.sh base
```
Start the mobile station:
```bash
./run.sh mobile
```

## Test the network

### Throughput test
To run the throughput test, run the following scripts:

1. Start the iperf3 server on the base station:
```
python3 test/iperf3_server.py
```
2. Start the test on the mobile station:
```
./run.sh tTest
```
The result is printed into the console and then saved into a file [/results/throughput-rho.txt](/test/results/throughput-rho.txt), and a plot is produced at [plots/throughput-rho.png](/test/plots/throughput-rho.png) as such:

![plots/throughput-rho.png](/test/plots/throughput-rho.png) 

---

### Latency test
To run the Latency test, run the following scripts:

1. Start the udp server on the base station:
```
python3 test/udp_server.py
```
2. Start the test on the mobile station:
```
./run.sh lTest
```

The result is printed into the console and then saved into a file [/results/latency-rho.txt](/test/results/latency-rho.txt), and a plot is produced at [plots/latency-rho.png](/test/plots/latency-rho.png) as such:

![latency-rho.png](/test/plots/latency-rho.png)
