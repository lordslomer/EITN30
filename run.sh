#!/bin/bash
if [ $1 = "base" ]
then
  sudo iptables -F
  sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
  sudo iptables -A FORWARD -i wlan0 -o myG -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A FORWARD -i myG -o wlan0 -j ACCEPT
  sudo python3 main.py --unit 0
elif [ $1 = "mobile" ]
then
  sudo python3 main.py --unit 1
fi