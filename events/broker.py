
MAX_NUMBER_OF_ELEMENT = 20
BLOCKING = 1
NON_BLOCKING = 2

class Broker:
   def __init__(self, mode):
      self.mode = mode
      self.queue = []
      self.writeIndex = 0
      self.readIndex = 0
      self.numberOfElementInserted = 0

   def dispatch(self, message):
      if(self.mode == BLOCKING):
         self.dispatchBlocking(message)
      elif(self.mode == NON_BLOCKING):
         self.dispatchNonBlocking(message)

   def dispatchBlocking(self, message):
      pass

   def dispatchNonBlocking(self, message):
      self.queue.append(message)
      self.writeIndex += int(1)
      if(self.writeIndex == MAX_NUMBER_OF_ELEMENT):
         self.writeIndex = int(0)
      self.numberOfElementInserted += int(1)

   def manager(self):
      if(self.numberOfElementInserted > 0):
         message = self.queue(self.readIndex)
         self.readIndex += int(1)
         if(self.writeIndex == MAX_NUMBER_OF_ELEMENT):
            self.writeIndex = int(0)
         self.dispatch(message)

broker = Broker(BLOCKING)

def broker_setDispatchFunction(func):
   broker.dispatchBlocking = func