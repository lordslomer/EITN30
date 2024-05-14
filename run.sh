#!/bin/bash
if [ $1 = "base" ]
then
  sudo iptables -F
  sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
  sudo iptables -A FORWARD -i eth0 -o myG -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A FORWARD -i myG -o eth0 -j ACCEPT
  sudo python3 src/main.py --unit 0
elif [ $1 = "mobile" ]
then
  sudo python3 src/main.py --unit 1
elif [ $1 = "iperf3 s" ]
then
  sudo python3 test/iperf3_server.py 
elif [ $1 = "iperf3 c" ]
then
  sudo python3 test/iperf3_client.py 
fi