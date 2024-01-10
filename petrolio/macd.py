
import yfinance as yf
import numpy as np
import tensorflow
import matplotlib.pyplot as plt
import pandas_ta as ta
import pandas as pd
import math
import copy
from pathlib import Path
import os

'''
goal:
- high global gain
- keep open position opened for as few days as possible
- high win/lose ratio

'''

PATH_LOG = "C:/Users/Marco/Documents/python/petrolio/log.txt"

#############################
#  private classes
#############################
class Order:
   def __init__(self):
      #self.currentlyHaveAnOrder = False
      self.openPrice = 0
      self.closePrice = 0
      self.openAt = 0
      self.closeAt = 0
   
   def Reset(self):
      #self.currentlyHaveAnOrder = False
      self.openPrice = 0
      self.closePrice = 0
      self.openAt = 0
      self.closeAt = 0

class Status:
   def __init__(self):
      self.macdUnderSignal_previous = True
      self.macdUnderSignal_current = True
      self.currentlyHaveAnOrder = False
      self.macdIsNegative_previous = False
      self.macdIsNegative_current = False
      self.numberOfBuySignals = 0
      self.numberOfSellSignals = 0

   def UpdateStatus(self, currentMACD, currentSignal):
      if(currentMACD > currentSignal):
         self.macdUnderSignal_current = False
      else:
         self.macdUnderSignal_current = True

      if(currentMACD > 0):
         self.macdIsNegative_current = True

   def UpdateAtTheEnd(self):
      self.macdUnderSignal_previous = self.macdUnderSignal_current
      self.macdIsNegative_previous = self.macdIsNegative_current

   def GenerateBuySignal(self):
      if(self.macdIsNegative_current == False and self.macdIsNegative_previous == True):
         return True
      if(self.macdUnderSignal_current == False and self.macdUnderSignal_previous == True):
         return True
      return False
      
   def GenerateSellSignal(self):
      if(self.macdIsNegative_current == True and self.macdIsNegative_previous == False):
         return True
      if(self.macdUnderSignal_current == True and self.macdUnderSignal_previous == False):
         return True
      return False

   def Reset(self):
      self.macdUnderSignal_previous = True
      self.macdUnderSignal_current = True
      self.currentlyHaveAnOrder = False
      self.macdIsNegative_previous = False
      self.macdIsNegative_current = False
      self.numberOfBuySignals = 0
      self.numberOfSellSignals = 0

class LogData:
   def __init__(self):
      self.fastParam = 0
      self.slowParam = 0
      self.signalParam = 0
      self.openDays = 0
      self.globalGain = 0
      self.goodTrades = 0
      self.badTrades = 0
      self.numberOfBuySignals = 0

#############################
#  private methods
#############################

def Load():
   
   matrix = []

   path = "C:/Users/Marco/Documents/python/petrolio/Future Petrolio Brent Dati Storici.csv"
   f = open(path, 'r')
   lines = f.readlines()
   '''
   for i in range(1, len(lines)):
      data = lines[i].split("\",\"")
      array = []
      n = data[1].replace('\'', '')
      array.append(float(data[1].replace('\'', '').replace(',','.')))
      array.append(float(data[2].replace('\'', '').replace(',','.')))
      array.append(float(data[3].replace('\'', '').replace(',','.')))
      array.append(float(data[4].replace('\'', '').replace(',','.')))
      matrix.append(array)
   
   matrix.remove(matrix[0])   #tolgo prima riga
   '''
   for i in range(len(lines)-1, 0, -1):
      data = lines[i].split("\",\"")
      array = []
      n = data[1].replace('\'', '')
      array.append(float(data[1].replace('\'', '').replace(',','.')))
      array.append(float(data[2].replace('\'', '').replace(',','.')))
      array.append(float(data[3].replace('\'', '').replace(',','.')))
      array.append(float(data[4].replace('\'', '').replace(',','.')))
      matrix.append(array)

   matrix = np.array(matrix)

   return matrix

def AnalizeOrders(orders):
   
   openDays = 0
   globalGain = 0
   goodTrades = 0
   badTrades = 0

   for order in orders:
      openDays += int(int(order.closeAt) - int(order.openAt))
      gain = float(float(order.closePrice) - float(order.openPrice))
      globalGain += gain

      if(gain > 0):
         goodTrades += 1
      else:
         badTrades += 1

   #print("open days: {0}".format(openDays))
   #print("global gain: {0}".format(globalGain))
   #print("good trades: {0}".format(goodTrades))
   #print("bad trades: {0}".format(badTrades))

   return (openDays, globalGain, goodTrades, badTrades)

def WriteLog(logData):
   line = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(logData.fastParam,
                                                logData.slowParam, 
                                                logData.signalParam, 
                                                logData.openDays, 
                                                logData.globalGain, 
                                                logData.goodTrades, 
                                                logData.badTrades,
                                                logData.numberOfBuySignals,
                                                logData.closeAt)
   f = open(PATH_LOG, "a")
   f.write(line)
   f.close()

def ComputeMACD(data, fast, slow, signal):
   df = pd.DataFrame(data, columns = ['a'])
   porcodio = ta.macd(df.a, fast = fast, slow = slow, signal = signal)
   porcodio = np.array(porcodio)
   return porcodio

def IfLogFileExistsDeleteIt():
   my_file = Path(PATH_LOG)
   if my_file.is_file():
      os.remove(PATH_LOG)

def GetValueFromLines(lines, whichValue):
   array = []
   
   for line in lines:
      data = line.split(',')
      array.append(int(data[whichValue]))

   array = np.array(array)
   return array

#############################
#  public methods
#############################
def createLog():
   data = Load()
   #help(ta.macd)

   close = data[-365:, 0]
   length = close.shape[0]

   #IfLogFileExistsDeleteIt()

   events = []

   for fastParam in range(1, 25):
      for slowParam in range (fastParam, 40):
         for signalParam in range (0, 15):
            for closeAt in range (0, 10, 1):
               fastParam = 12
               slowParam = 26
               signalParam = 9

               macdData = ComputeMACD(close, fastParam, slowParam, signalParam)

               macd = macdData[:, 0]
               histogram = macdData[:, 1]
               signal = macdData[:, 2]
               #delta = histogram - macd + signal  #ok porco dio almeno questo è 0
               
               plt.plot(macd, 'r')
               #plt.plot(histogram, 'g')
               plt.plot(signal, 'b')
               plt.plot(close)
               #plt.show()
               
               order = Order()
               status = Status()
               orders = []

               for i in range(0, length-1):
                  if(math.isnan(macd[i]) == False and math.isnan(signal[i]) == False):
                     status.UpdateStatus(macd[i], signal[i])

                     buySignal = status.GenerateBuySignal()
                     sellSignal = status.GenerateSellSignal()

                     if(buySignal == True):
                        status.numberOfBuySignals += int(1)

                     if(status.currentlyHaveAnOrder == False):
                        if(buySignal == True):
                           #buySignal = False
                           status.currentlyHaveAnOrder = True
                           order.openPrice = close[i]
                           order.openAt = i
                     else:
                        #if(sellSignal == True):
                        if(close[i] > order.openPrice + 0.01 or close[i] < order.openPrice - 1):
                        #if(close[i] > order.openPrice + 0.01):
                        #if(close[i] > order.openPrice + 0.01 or close[i] < order.openPrice - closeAt):
                           order.closePrice = close[i]
                           status.currentlyHaveAnOrder = False
                           order.closeAt = i
                           orders.append(copy.deepcopy(order))
                           order.Reset()

                     if(status.currentlyHaveAnOrder == True):
                        events.append(1)
                     else:
                        events.append(0)
                     
                     status.UpdateAtTheEnd()
                  else:
                     events.append(0)

               plt.plot(events)
               plt.show()

               openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)

               logData = LogData()
               logData.openDays = openDays
               logData.globalGain = globalGain
               logData.goodTrades = goodTrades
               logData.badTrades = badTrades
               logData.fastParam = fastParam
               logData.slowParam = slowParam
               logData.signalParam = signalParam
               logData.closeAt = closeAt
               logData.numberOfBuySignals = status.numberOfBuySignals

               WriteLog(logData)

def AnalyzeLog():
   f = open(PATH_LOG, "r")
   lines = f.readlines()

   globalGain = [] 
   
   for line in lines:
      data = line.split(',')
      globalGain.append(float(data[4]))

   openDays = GetValueFromLines(lines, 3)
   globalGain = np.array(globalGain)
   goodTrades = GetValueFromLines(lines, 5)
   badTrades = GetValueFromLines(lines, 6)
   numberOfBuySignals = GetValueFromLines(lines, 7)
   
   points = []

   for i in range(globalGain.shape[0]):
      if(globalGain[i] < 0):
         points.append(0)
      else:
         winRate = goodTrades[i] / (goodTrades[i] + badTrades[i])
         result = globalGain[i] * winRate / openDays[i]
         points.append(result)

   plt.plot(points, 'o')
   plt.xlabel("entry number")
   plt.ylabel("points")
   plt.show()
   '''
   plt.plot(openDays, globalGain, 'o')
   plt.xlabel("open days")
   plt.ylabel("global gain")
   plt.show()

   plt.figure()
   plt.plot(goodTrades, globalGain, 'o')
   plt.xlabel("good trades")
   plt.ylabel("global gain")
   plt.show()

   plt.figure()
   plt.plot(numberOfBuySignals, goodTrades, 'o')
   plt.xlabel("number of buy signal")
   plt.ylabel("good trades")
   plt.xlim(0, 100)
   plt.ylim(0, 100)
   plt.show()

   plt.figure()
   winRate = goodTrades / (goodTrades + badTrades)
   plt.plot(winRate, 'o')
   plt.xlabel("win rates")
   #plt.ylabel("good trades")
   plt.show()
   '''
   plt.pause(1)


if __name__ == "__main__":
   #createLog()
   AnalyzeLog()