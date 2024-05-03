import threading
import time
import queue

class Queue:
  def __init__(self, name) -> None:
    self.q = queue.Queue()
    self.name = name
    self.t0_in = time.time()
    self.t0_out = time.time()
    self.ctn_in = 0
    self.ctn_out = 0
  
  def put(self, bytes):
    self.q.put(bytes)
    t1 = time.time()
    durr = t1 - self.t0_in
    self.ctn_in+=1
    if durr >= 1:
      # print(self.name, "inflöde :",self.ctn_in/durr)
      self.t0_in = t1
      self.ctn_in = 0


  def pop(self):
    temp = self.q.get()
    t1 = time.time()
    durr = t1 - self.t0_out
    self.ctn_out+=1
    if durr >= 1:
      # print(self.name, "utflöde :", self.ctn_out/durr)
      self.t0_out = t1
      self.ctn_out = 0
    return temp