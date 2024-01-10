
from broker import *
from messages import *

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


class SupportAndResistance:
   def __init__(self):
      self.lastThreePoints = []
      self.maxPoints = TwoElementQueue()
      self.minPoints = TwoElementQueue()
      self.isInHysteresisregion = False
      self.callback = self.cb_Idle
      self.lastReceivedData = None

   def manager(self):
      self.callback()

   def messageHandler(self, message):
      if(message.header.type == NEW_DATA_ARRIVED):
         self.lastReceivedData = message.payload
         data = message.payload["ultimo"]
         time = message.payload["time"]
         entry = Entry(time, data)
         entry.absoluteTimestamp = message.payload["time"]["tempo assoluto"]
         self.lastThreePoints.append(entry)
         
         if(len(self.lastThreePoints) > 3):
            self.lastThreePoints.pop(0)

         if(len(self.lastThreePoints) == 3):
            first = self.lastThreePoints[0].value
            second = self.lastThreePoints[1].value
            third = self.lastThreePoints[2].value

            if(detectMax(first, second, third) == True):
               self.maxPoints.addItem(self.lastThreePoints[1])

            if(detectMin(first, second, third) == True):
               self.minPoints.addItem(self.lastThreePoints[1])
            """
            currentPosition = float(data)

            if(len(self.maxPoints.queue) == 2):
               m, q = self.maxPoints.computeSlopeAndInterceptor()

               currentPositionMaxLine = float(entry.absoluteTimestamp) * float(m) + float(q)

               if(self.isInHysteresisregion == False):
                  if(currentPosition < currentPositionMaxLine + 0.0003 and currentPosition > currentPositionMaxLine - 0.0003):
                     self.isInHysteresisregion = True
               else:
                  if(currentPosition > currentPositionMaxLine + 0.0003):
                     #ha decisamente sfondato il limite superiore
                     sendBuyOrder(self.lastReceivedData)
                  if(currentPosition < currentPositionMaxLine - 0.0003):
                     #ha sfondato il limite ma sta tornando indietro
                     sendSellOrder(self.lastReceivedData)
                     
            if(len(self.minPoints.queue) == 2):
               m, q = self.minPoints.computeSlopeAndInterceptor()

               currentPositionMinLine = float(entry.absoluteTimestamp) * float(m) + float(q)

               if(self.isInHysteresisregion == False):
                  if(currentPosition < currentPositionMinLine + 0.0003 and currentPosition > currentPositionMinLine - 0.0003):
                     self.isInHysteresisregion = True
               else:
                  if(currentPosition > currentPositionMinLine + 0.0003):
                     #ha decisamente sfondato il limite superiore
                     #sendBuyOrder(currentPosition)
                     pass
                  if(currentPosition < currentPositionMinLine - 0.0003):
                     #ha sfondato il limite ma sta tornando indietro
                     #sendSellOrder(currentPosition)
                     pass
            """

      elif(message.header.type == RESET):
         self.__init__()
    

   def cb_inIdleRegion(self):
      self.callback = self.computeNextState()      

   def cb_inUpperHysteresisRegion(self):
      self.callback = self.computeNextState()

      if(self.callback == self.cb_inIdleRegion):
         sendSellOrder(self.lastReceivedData)
      
   def cb_overUpperHysteresisRegion(self):
      sendBuyOrder(self.lastReceivedData)
      self.callback = self.computeNextState()
      
   def cb_inUnderHysteresisRegion(self):
      self.callback = self.computeNextState()      

      if(self.callback == self.cb_inIdleRegion):
         sendBuyOrder(self.lastReceivedData)
      
   def cb_underUnderHysteresisRegion(self):
      sendSellOrder(self.lastReceivedData)
      self.callback = self.computeNextState()
      
   def cb_Idle(self):
      if(len(self.maxPoints.queue) == 2 and 
         len(self.minPoints.queue) == 2 and
         len(self.lastThreePoints) == 3):
         self.callback = self.computeNextState()


   def computeNextState(self):
      if(self.lastReceivedData != None):
         currentPosition = self.lastReceivedData["ultimo"]
         currentAbsoluteTimeStamp = self.lastReceivedData["time"]["tempo assoluto"]

         m, q = self.maxPoints.computeSlopeAndInterceptor()
         currentPositionMaxLine = float(currentAbsoluteTimeStamp) * float(m) + float(q)

         m, q = self.minPoints.computeSlopeAndInterceptor()
         currentPositionMinLine = float(currentAbsoluteTimeStamp) * float(m) + float(q)

         hysteresis = float(0.0005)

         if(currentPosition > currentPositionMaxLine + hysteresis):
            nextState = self.cb_overUpperHysteresisRegion
         elif(currentPosition > currentPositionMaxLine - hysteresis and currentPosition <= currentPositionMaxLine + hysteresis):
            nextState = self.cb_inUpperHysteresisRegion
         elif(currentPosition <= currentPositionMaxLine - hysteresis and currentPosition >= currentPositionMinLine + hysteresis):
            nextState = self.cb_inIdleRegion
         elif(currentPosition >= currentPositionMinLine - hysteresis and currentPosition < currentPositionMinLine + hysteresis):
            nextState = self.cb_inUnderHysteresisRegion
         elif(currentPosition < currentPositionMinLine - hysteresis):
            nextState = self.cb_underUnderHysteresisRegion
         
         return nextState
      else:
         return self.callback


def sendBuyOrder(lastData):
   value = lastData["ultimo"]
   dataTime = lastData["time"]
   sendOrder(SIGNAL_BUY, value, dataTime)

def sendSellOrder(lastData):
   value = lastData["ultimo"]
   dataTime = lastData["time"]
   sendOrder(SIGNAL_SELL, value, dataTime)
 
def sendOrder(orderType, data, time):
   message = Message()
   message.header.sender = SENDER_ALGORITHM
   
   message.header.type = orderType
   
   dictionary = {
      "value": data,
      "time": time
   }
   
   message.payload = dictionary
   broker.dispatch(message)

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

   
supportAndResistance = SupportAndResistance()

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
   


