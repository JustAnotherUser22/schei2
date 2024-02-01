
from broker import *
from messages import *
from algorithmsFolder.supportAndResistance import supportAndResistance
from algorithmsFolder.MovingAverage import MovingAverage


class Entry:
   def __init__(self, timestamp, value):
      self.timestamp = timestamp    #stringa che rappresenta il timestamp
      self.value = value
      self.absoluteTimestamp = 0    #valore temporale "globale" (x es 1h = 3600, 5m = 300...)
      
class TwoElementQueue:
   def __init__(self):
      self.queue = []

   def addItem(self, item):
      self.queue.append(item)

      if(len(self.queue) > 2):
         self.queue.pop(0)
   
   def computeSlopeAndInterceptor(self):
      
      firstPoint = self.queue[0]
      secondPoint = self.queue[1]
              
      x0 = float(firstPoint.absoluteTimestamp)
      y0 = float(firstPoint.value)
      x1 = float(secondPoint.absoluteTimestamp)
      y1 = float(secondPoint.value)
      m = computeSlope(x0, y0, x1, y1)
      q = computeInterceptor(x0, y0, m)

      return m, q


class Algorithm:
   def __init__(self, broker):
      self.localAlgo = MovingAverage(broker)
      self.broker = broker
      
   def manager(self):
      #self.localAlgo.manager()
      if(self.localAlgo.needToBuy == True):
         self.sendBuyOrder(self.localAlgo.lastValue)
         self.localAlgo.needToBuy = False

      if(self.localAlgo.needToSell == True):
         self.sendSellOrder(self.localAlgo.lastValue)
         self.localAlgo.needToSell = False
      
   def messageHandler(self, message):
      self.localAlgo.messageHandler(message)


   def sendBuyOrder(self, lastData):
      value = lastData["value"]
      dataTime = lastData["time"]
      self.sendOrder(SIGNAL_BUY, value, dataTime)

   def sendSellOrder(self, lastData):
      value = lastData["value"]
      dataTime = lastData["time"]
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

   
#algorithm = Algorithm()

#############################
#  funzioni locali per il funzionamento dell'algoritmo
############################

def computeSlope(x0, y0, x1, y1):
   return (y0 - y1) / (x0 - x1)

def computeInterceptor(x0, y0, m):
   return y0 - m * x0

def detectMax(first, second, third):
   if(second > first and second > third):
      return True
   else:
      return False
   
def detectMin(first, second, third):
   if(second < first and second < third):
      return True
   else:
      return False
   


