# EITN30 - Internet Inuti

## Start the network
If you cannot execute *run.sh*, make the bash script execuatble: 
```
chmod +x run.sh
```

run the base station:
```bash
./run.sh base
```
run the mobile station:
```bash
./run.sh mobile
```

## Test the network

### Throughput test
To run the throughput test, run the following scripts in the `/test` directory:

1. Start the iperf3 server on the base station
```
python3 iperf3_server.py
```
2. Start the test on the mobile station
```
python iperf3_client.py
```
The result of each individual test is printed into the consoles, and a plot is produced at `/plots/throughput-rho.pdf`

### Latency test
To run the Latency test, run the following scripts in the `/test` directory:

1. Start the iperf3 server on the base station
```
python3 udp_server.py
```
2. Start the test on the mobile station
```
python udp_client.py
```
The result of each individual test is printed into the consoles, and a plot is produced at `/plots/latency-rho.pdf`
