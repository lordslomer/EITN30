import threading
import time
import queue

class Queue:
  def __init__(self, name) -> None:
    self.q = queue.Queue()
    self.name = name
    self.t0_in =  time.time()
    self.t0_out = self.t0_in
    self.ctn_in = 0
    self.ctn_out = 0
  
  def put(self, bytes):
    self.q.put(bytes)
    t1 = time.time()
    durr = t1 - self.t0_in
    self.ctn_in+=len(bytes)*8
    if durr >= 1:
      speed = self.ctn_in/durr
      print(self.name, f"in-rate:  {speed if speed < 1000 else speed/1000:.2f}", "Kbps" if speed > 1000 else "bps")
      self.t0_in = t1
      self.ctn_in = 0


  def pop(self):
    temp = self.q.get()
    t1 = time.time()
    durr = t1 - self.t0_out
    self.ctn_out+=len(temp)*8
    if durr >= 1:
      speed = self.ctn_out/durr
      print(self.name, f"out-rate: {speed if speed < 1000 else speed/1000:.2f}", "Kbps" if speed > 1000 else "bps","\n")
      self.t0_out = t1
      self.ctn_out = 0
    return temp