
from data import *
from algorithm import *
from broker import *
from messages import *
from manager import *
from history import *
from plotter import *
import matplotlib.pyplot as plt



class Test:
   
   def __init__(self):
      self.localValue = 0
      self.broker = 0

   def publish(self, value):
      message = Message()
      message.header.sender = SENDER_DATA
      message.header.type = NEW_DATA_ARRIVED
      message.value = value
      self.broker.dispatch(message)

   def messageHandler(self, message):
      self.localValue = message.value

def miniTest():
   localBroker = Broker(WITH_PROCESS)
   test = Test()
   
   test.broker = localBroker
   
   localBroker.subscribers.append(test)
   
   test.publish(666)

   print(test.localValue)


def mainWithProcess():
   
   localBroker = Broker(WITH_PROCESS)
   localData = DataReader()
   localManager = Manager()
   localHistory = History()
   localAlgorithm = Algorithm()

   localData.broker = localBroker
   localManager.broker = localBroker
   localHistory.broker = localBroker
   localAlgorithm.broker = localBroker

   localBroker.subscribers.append(localData)
   localBroker.subscribers.append(localManager)
   localBroker.subscribers.append(localHistory)
   localBroker.subscribers.append(localAlgorithm)

   while(localData.dataEnded == False):
      localData.manager()
      algorithm.manager()
      manager.manager()
      history.manager()

   #history.printAll()
   history.printFinalGain()



if __name__ == "__main__":
   #miniTest()
   mainWithProcess()