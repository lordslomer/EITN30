import threading
import time
import queue

class Queue:
  def __init__(self, name, verbose=False) -> None:
    self.q = queue.Queue()
    self.verbose = verbose
    self.name = name
    self.t0_in =  time.time()
    self.t0_out = self.t0_in
    self.out_rate = 0
    self.in_rate = 0
    self.ctn_out = 0
    self.ctn_in = 0
  
  def put(self, bytes):
    self.q.put(bytes)

    # inc metrics
    t1 = time.time()
    durr = t1 - self.t0_in
    self.ctn_in+=len(bytes)*8

    if durr >= 1:
      # use metrics to estimate the incoming rate for the last sec
      self.in_rate = self.ctn_in/durr

      if self.verbose:
        print(self.name, f": {self.in_rate/1000:.3f} Kbps ----> {self.out_rate/1000:.3f} Kbps\n")

      # reset metrics
      self.t0_in = t1
      self.ctn_in = 0


  def pop(self):
    last = self.q.get()

    # inc metrics
    t1 = time.time()
    durr = t1 - self.t0_out
    self.ctn_out+=len(last)*8

    if durr >= 1:
      # use metrics to estimate the outgoing rate for the last sec
      self.out_rate = self.ctn_out/durr

      # reset metrics
      self.t0_out = t1
      self.ctn_out = 0
    return last