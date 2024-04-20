#!/bin/bash
if [ $1 = "base" ]
then
  sudo ip link delete myG
  sudo iptables -F
  sudo iptables -t nat -A POSTROUTING -o myG -j MASQUERADE
  sudo iptables -A FORWARD -i eth0 -o myG -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A FORWARD -i myG -o eth0 -j ACCEPT
  sudo python3 main.py --unit 0
elif [ $1 = "mobile" ]
then
  sudo ip link delete myG 
  sudo iptables -F
  sudo iptables -A INPUT -i myG -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A OUTPUT -o myG -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT
  sudo python3 main.py --unit 1
fi