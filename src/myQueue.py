import threading
import time
import queue

class Queue:
  def __init__(self, name, verbose=False) -> None:
    self.q = queue.Queue()
    self.name = name
    self.t0_in =  time.time()
    self.t0_out = self.t0_in
    self.ctn_in = 0
    self.ctn_out = 0
    self.in_rate = 0
    self.out_rate = 0
    self.verbose = verbose
  
  def put(self, bytes):
    self.q.put(bytes)
    t1 = time.time()
    durr = t1 - self.t0_in
    self.ctn_in+=len(bytes)*8
    if durr >= 1:
      self.in_rate = self.ctn_in/durr
      if self.out_rate > 0 and self.in_rate/self.out_rate > 1.1:
        if self.verbose:
          print(self.name, f": {self.__format_speed(self.in_rate)} - {self.q.qsize()*1.5} {self.out_rate/8000:.2f}-> {self.__format_speed(self.out_rate)}\n")
      self.t0_in = t1
      self.ctn_in = 0


  def pop(self):
    temp = self.q.get()
    t1 = time.time()
    durr = t1 - self.t0_out
    self.ctn_out+=len(temp)*8
    if durr >= 1:
      self.out_rate = self.ctn_out/durr
      self.t0_out = t1
      self.ctn_out = 0
    return temp
  
  def __format_speed(self, speed):
    return f"{speed if speed < 1000 else speed/1000:.2f}" + (" Kbps" if speed > 1000 else " bps")