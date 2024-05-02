import threading


class Queue:
  def __init__(self) -> None:
    self.q = []
    self.l = threading.Condition()
    pass
  
  def put(self, bytes):
    with self.l:
      self.q.append(bytes)
      self.l.notify_all()

  def pop(self):
    with self.l:
      while len(self.q) <= 0:
        self.l.wait()
      return self.q.pop()
    