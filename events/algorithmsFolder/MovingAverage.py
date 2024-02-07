
#from broker import *
from messages import *


class MovingAverage:
   def __init__(self, broker):
      self.array = []
      self.stabilityCounter = int(0)
      self.NUMBER_OF_SAMPLES = 100
      self.THRESHOLD = 15
      self.callback = self.cb_idle
      
      self.needToBuy = False
      self.needToSell = False
      self.lastValue = 0

      self.broker = broker

   def manager(self):
      #eseguo operazioni solo quando arriva un nuovo dato
      pass
      
   def messageHandler(self, message):
      if(message.header.type == NEW_DATA_ARRIVED):
         data = message.payload["ultimo"]
         time = message.payload["time"]
         self.array.append(data)

         if(len(self.array) > self.NUMBER_OF_SAMPLES):
            self.array.pop(0)
            average = Average(self.array)
            self.publicNewMACDEntry(average)
            if(data > average):
               if(self.callback != self.cb_signalOverAverage):
                  self.stabilityCounter = 0
               self.callback = self.cb_signalOverAverage
            else:
               if(self.callback != self.cb_signalUnderAverage):
                  self.stabilityCounter = 0
               self.callback = self.cb_signalUnderAverage
            self.callback(data, time)

      elif(message.header.type == RESET):
         self.__init__()

   def cb_idle(self):
      return

   def cb_signalOverAverage(self, value, time):
      self.stabilityCounter += int(1)
      self.needToBuy = False
      self.needToSell = False
      if(self.stabilityCounter > self.THRESHOLD):
         self.sendBuyOrder(value, time)
         '''
         self.needToBuy = True
         self.lastValue = {
                              "value": value,
                              "time": time
                           }
         '''
         
   
   def cb_signalUnderAverage(self, value, time):
      self.stabilityCounter += int(1)
      self.needToBuy = False
      self.needToSell = False
      
      if(self.stabilityCounter > self.THRESHOLD):
         self.sendSellOrder(value, time)
         '''
         self.needToSell = True
         self.lastValue = {
                              "value": value,
                              "time": time
                           }
         '''
         
         
   def publicNewMACDEntry(self, data):
      message = Message()
      message.header.type = NEW_MOVING_AVERAGE_COMPUTED
   
      dictionary = {
         "value": data,
      }
      
      message.payload = dictionary
      self.broker.dispatch(message)


   def sendBuyOrder(self, value, dataTime):
      self.sendOrder(SIGNAL_BUY, value, dataTime)

   def sendSellOrder(self, value, dataTime):
      self.sendOrder(SIGNAL_SELL, value, dataTime)
   
   def sendOrder(self, orderType, data, time):
      message = Message()
      message.header.sender = SENDER_ALGORITHM
      
      message.header.type = orderType
      
      dictionary = {
         "value": data,
         "time": time
      }
      
      message.payload = dictionary
      self.broker.dispatch(message)



'''
il messaggio è di questo tipo

header : {
   sender: SENDER_ALGORITHM
   type: "sell" oppure "buy"
}  
payload : {
   "value": valore a cui si apre la posizione,
   "time": dizionario con i dati temporali
} 

'''

   
#movingAverage = MovingAverage()


def Average(lst):
    return sum(lst) / len(lst)


