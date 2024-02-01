
from broker import *
from messages import *
from order import *

'''
storico delle operazioni,
quando una posizione viene chiusa questo la salva in una coda
'''



class Balance:
   def __init__(self):
      self.base = 0
      self.quote = 0
      

   def manageOrder(self, order):

      size = int(1)

      if(order.positionType == "buy"):
         self.base += int(1) * size
         self.quote -= order.openValue * size
         self.base -= int(1) * size
         self.quote += order.closeValue * size
      if(order.positionType == "sell"):
         self.base -= int(1) * size
         self.quote += order.openValue * size
         self.base += int(1) * size
         self.quote -= order.closeValue   * size
      


class History:
   def __init__(self, broker):
      self.allOrders = []
      self.balance = Balance()
      self.line = ""
      self.broker = broker

   def printAll(self):
      for element in self.allOrders:
         delta = '{0:.7f}'.format(element.closeValue - element.openValue)
         open = '{0:.7f}'.format(element.openValue)
         close = '{0:.7f}'.format(element.closeValue)
         type = element.positionType

         print("enter at: {1}   exit at: {2}   delta = {3}    type:{0}".format(type, open, close , delta))

   def printFinalGain(self):
      for element in self.allOrders:
         self.balance.manageOrder(element)
      #print("base = {0}     quote = {1}".format(round(self.balance.base, 4), round(self.balance.quote, 5)))

      numberOfGoodTrades = 0
      numberOfBadTrades = 0
      
      for element in self.allOrders:
         if(element.positionType == "buy"):
            if(element.closeValue > element.openValue):
               numberOfGoodTrades += int(1)
            else:
               numberOfBadTrades += int(1)
         elif(element.positionType == "sell"):
            if(element.openValue > element.closeValue):
               numberOfGoodTrades += int(1)
            else:
               numberOfBadTrades += int(1)
      
      wr = 0

      if(numberOfGoodTrades != 0 or numberOfBadTrades != 0):
         wr = numberOfGoodTrades / (numberOfGoodTrades + numberOfBadTrades)
      print("good trades = {0}   bad trades = {1}   win rate = {2:.3f}".format(numberOfGoodTrades, numberOfBadTrades, wr))
      #print("win rate = {0:.3f}".format(numberOfGoodTrades / (numberOfGoodTrades + numberOfBadTrades)))
      self.line = "{0},{1},{2}".format(numberOfGoodTrades, numberOfBadTrades, wr)
   

   def manager(self):
      return 0;

   def messageHandler(self, message):
      if(message.header.type == ORDER_HAS_BEEN_CLOSED):
         self.allOrders.append(message.payload)
      elif(message.header.type == RESET):
         self.__init__()


#history = History()

