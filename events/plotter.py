from broker import *
from messages import *

class Point:
   def __init__(self, x, y):
      self.x = x
      self.y = y

class MacdData:
   def __init__(self):
      self.macd = []
      self.histogram = []
      self.signal = []
      

class Plotter:
   def __init__(self):
      self.allData = []
      self.dataCounter = 0
      self.openPositions = []
      self.closePositions = []
      self.movingAverageData = []
      self.macdData = MacdData()
      
   #def manager(self):
   #   self.callback()

   def messageHandler(self, message):
      if(message.header.type == NEW_DATA_ARRIVED):
         self.allData.append(message.payload["ultimo"])
         self.dataCounter += int(1)

      elif(message.header.type == ORDER_HAS_BEEN_CLOSED):
         openPositionTime = message.payload.openedAtTime["tempo assoluto"]
         openPositionValue = message.payload.openValue
         closePositionTime = message.payload.closedAtTime["tempo assoluto"]
         closePositionValue = message.payload.closeValue

         self.openPositions.append(Point(openPositionTime, openPositionValue))
         self.closePositions.append(Point(closePositionTime, closePositionValue))

      elif(message.header.type == NEW_MOVING_AVERAGE_COMPUTED):
         self.movingAverageData.append(message.payload["value"])

      elif(message.header.type == NEW_MACD_COMPUTED):
         self.macdData.macd.append(message.payload["macd"])
         self.macdData.histogram.append(message.payload["histogram"])
         self.macdData.signal.append(message.payload["signal"])
         
      elif(message.header.type == RESET):
         self.__init__()
         
   
#plotter = Plotter()