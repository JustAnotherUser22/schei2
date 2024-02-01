
MAX_NUMBER_OF_ELEMENT = 20
BLOCKING = 1
NON_BLOCKING = 2
WITH_PROCESS = 3

class Broker:
   def __init__(self, mode):
      self.mode = mode
      self.queue = []
      self.writeIndex = 0
      self.readIndex = 0
      self.numberOfElementInserted = 0
      self.subscribers = []

   def dispatch(self, message):
      if(self.mode == BLOCKING):
         self.dispatchBlocking(message)
      elif(self.mode == NON_BLOCKING):
         self.dispatchNonBlocking(message)
      elif(self.mode == WITH_PROCESS):
         self.dispatchWithProcess(message)

   def dispatchWithProcess(self, message):
      for element in self.subscribers:
         element.messageHandler(message)

   def dispatchBlocking(self, message):
      #pass
      for element in self.subscribers:
         element.messageHandler(message)

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

#broker = Broker(BLOCKING)

def broker_setDispatchFunction(func):
   #broker.dispatchBlocking = func
   pass