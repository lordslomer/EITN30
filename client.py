import os
import socket
import time 
socket_addr = '10.0.0.1'
socket_port = 12739
socket_con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_con.settimeout(5)

def timeMicro():
   return int(time.time()*1000000)

seq_nbr = 1
total_bytes_sent = 0
start_time = time.time()
sleep_time = 0.01
try:
  while True:
    # construct and send payload
    payload = seq_nbr.to_bytes(4, 'big') + b"x" * 996
    socket_con.sendto(payload, (socket_addr, socket_port))
    duration = time.time() - start_time
    total_bytes_sent+=len(payload)

    if duration > 0:
      byterate = total_bytes_sent / duration 
      os.system('clear')
      print(f"{duration:.2f}", total_bytes_sent)
      print(f"{byterate:2f}")
      
    seq_nbr+=1
    time.sleep(sleep_time)

except socket.timeout:
    print("Request timed out.")
finally:
    socket_con.close()