#!/bin/bash
if [ $1 = "base" ]
then
  sudo iptables -F
  sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
  sudo iptables -A FORWARD -i eth0 -o myG -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A FORWARD -i myG -o eth0 -j ACCEPT
  # sudo g++ -std=c++11 -o main main.cpp -lrf24 -ltuntap && sudo ./main 0
  sudo python3 main.py --unit 0
elif [ $1 = "mobile" ]
then
  # sudo g++ -std=c++11 -o main main.cpp -lrf24 -ltuntap && sudo ./main 1
  sudo python3 main.py --unit 1
fi