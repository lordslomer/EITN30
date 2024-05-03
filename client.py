import socket
import time 
socket_addr = '10.0.0.1'
socket_port = 12739
socket_con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_con.settimeout(2)

seq_nbr = 0
time_stamp = int(time.time()*1000000)
try:
  payload = seq_nbr.to_bytes(4, 'big') + time_stamp.to_bytes(8, 'big')
  print(payload)
  socket_con.sendto(payload, (socket_addr, socket_port))
  
except socket.timeout:
  print("Server took too long to respond!")
finally:
  socket_con.close()