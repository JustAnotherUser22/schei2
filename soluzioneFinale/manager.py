

import order
from copy import deepcopy
from doubleEma import Doubleema
from datetime import datetime
from datetime import date



class Manager():

   def __init__(self, pd, config):
      self.currentState = self.cb_idle
      #self.close = close
      self.close = pd.iloc[:,1]
      self.dataframe = pd
      self.marketIsOpen = True
      
      #self.algo = Doubleema(close, config)
      self.algo = Doubleema(pd.iloc[:,1], config)
      self.signals = self.algo.signals
      self.order = order.Order()
      self.orders = []
      self.currentIndex = 0
      
   
   def scanData(self):
      '''
      funzione da chiamare a main
      '''
      for i in range(len(self.close)):
         self.currentIndex = i
         self.algo.currentIndex = i
         if(self.algo.allDataAreAvailable()):
            self.currentState()

   
   def cb_idle(self):
      i = self.currentIndex
      self.algo.currentIndex = i
      self.updateMarketState()
      if(self.marketIsOpen == True):
         if(self.algo.generateEntrySignal() == True):
            self.currentState = self.cb_haveOrder
            self.order.openValue = self.close[i]
            self.order.openedAtTime = i
            self.order.positionType = self.algo.signalGenerated


   def cb_haveOrder(self):
      i = self.currentIndex
      self.algo.currentIndex = i
      self.updateMarketState()
      if(self.marketIsOpen == True):
         if(self.algo.generateExitSignal() == True):
            self.currentState = self.cb_idle
            self.order.closeValue = self.close[i]
            self.order.closedAtTime = i
            self.orders.append(deepcopy(self.order))
            self.order.reset()

         now = self.dataframe.iloc[i, 0]
  
         data = now.split(' ')
         hour = int(data[1][0:2])
         minute = data[1][2:4]         

         if(hour == 16 and minute == 59):
            self.currentState = self.cb_idle
            self.order.closeValue = self.close[i]
            self.order.closedAtTime = i
            self.orders.append(deepcopy(self.order))
            self.order.reset()

         

   
   def updateMarketState(self):
      i = self.currentIndex
      now = self.dataframe.iloc[i, 0]

      isOpen = True

      data = now.split(' ')
      hour = int(data[1][0:2])
      minute = data[1][2:4]
      second = data[1][4:6]

      year = int(data[0][0:4])
      month = int(data[0][4:6])
      day = int(data[0][6:8])

      if(date(year = year, month = month, day = day).weekday() >= 5):
         isOpen = False

      if(hour > 17 and hour < 6):
         isOpen = False

      self.marketIsOpen = isOpen
      

   




