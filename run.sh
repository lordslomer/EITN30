#!/bin/bash
if [ $1 = "base" ]
then
  # Clear iptables
  sudo iptables -F
  
  # Translate the ip addrs outgoing from eth0 
  sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

  # Forward traffic eth0 -> myG
  sudo iptables -A FORWARD -i eth0 -o myG -m state --state RELATED,ESTABLISHED -j ACCEPT

  # Forward traffic myG -> eth0
  sudo iptables -A FORWARD -i myG -o eth0 -j ACCEPT

  # Start network as base station
  sudo python3 src/main.py --unit 0
elif [ $1 = "mobile" ]
then

  #  Start network as mobile station
  sudo python3 src/main.py --unit 1
elif [ $1 = "tTest" ]
then

  # Run throughput test script and plot the result.
  python3 test/iperf3_client.py
  python3 test/plotter.py t
elif [ $1 = "lTest" ]
then

  # Run latency test script and plot the result.
  python test/udp_client.py
  python3 test/plotter.py l
fi