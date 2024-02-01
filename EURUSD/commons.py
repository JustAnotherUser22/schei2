
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from ta.trend import MACD
from ta.trend import EMAIndicator
import math
from copy import deepcopy
from dataFolder import dataFiles

'''
file con funzioni comuni a entrambi i files
'''

class Status:
   def __init__(self):
      self.macdUnderSignal_previous = True
      self.macdUnderSignal_current = True
      self.currentlyHaveAnOrder = False
      self.macdIsNegative_previous = False
      self.macdIsNegative_current = False
      self.numberOfBuySignals = 0
      self.numberOfSellSignals = 0
      self.currentHistogram = 0
      self.currentEma = 0
      self.currentClose = 0

   def UpdateStatus(self, currentMACD, currentSignal, currentHistogram, currentEma, currentClose):
      if(currentMACD > currentSignal):
         self.macdUnderSignal_current = False
      else:
         self.macdUnderSignal_current = True

      if(currentMACD > 0):
         self.macdIsNegative_current = True

      self.currentHistogram = currentHistogram
      self.currentEma = currentEma
      self.currentClose = currentClose

   def UpdateAtTheEnd(self):
      self.macdUnderSignal_previous = self.macdUnderSignal_current
      self.macdIsNegative_previous = self.macdIsNegative_current

   def GenerateBuySignal(self):
      '''
      if(abs(self.currentHistogram) > 0.0001):
         #if(self.macdIsNegative_current == False and self.macdIsNegative_previous == True):
         #   return True
         if(self.macdUnderSignal_current == False and self.macdUnderSignal_previous == True):
            return True
      '''
      if(self.macdUnderSignal_current == False and self.macdUnderSignal_previous == True and self.currentClose > self.currentEma):
         return True
      return False
      
   def GenerateSellSignal(self):
      '''
      if(abs(self.currentHistogram) > 0.0001):
         #if(self.macdIsNegative_current == True and self.macdIsNegative_previous == False):
         #   return True
         if(self.macdUnderSignal_current == True and self.macdUnderSignal_previous == False):
            return True
      '''
      if(self.macdUnderSignal_current == True and self.macdUnderSignal_previous == False and self.currentClose < self.currentEma):
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


class Order:
   def __init__(self):
      #self.currentlyHaveAnOrder = False
      self.openPrice = 0
      self.closePrice = 0
      self.openAt = 0
      self.closeAt = 0
      self.operationType = 0
   
   def Reset(self):
      #self.currentlyHaveAnOrder = False
      self.openPrice = 0
      self.closePrice = 0
      self.openAt = 0
      self.closeAt = 0
      self.operationType = 0

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



def GetValueFromLines(lines, whichValue):
   array = []
   
   for line in lines:
      data = line.split(',')
      array.append(int(data[whichValue]))

   array = np.array(array)
   return array

def IfLogFileExistsDeleteIt(path):
   my_file = Path(path)
   if my_file.is_file():
      os.remove(path)

def LoadDataFromCSV(path):
   
   matrix = []

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

def AnalyzeLog(path):
   f = open(path, "r")
   lines = f.readlines()

   globalGain = [] 
   initialCapital = []
   
   for line in lines:
      data = line.split(',')
      globalGain.append(float(data[4]))

   globalGain.sort(reverse = True)

   for line in lines:
      data = line.split(',')
      initialCapital.append(float(data[10]))

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
         #result = winRate
         points.append(result)

   betterThanHalf = [i for i in points if i > 0.6]

   globalGain = np.array(globalGain)
   maxgg = max(globalGain)

   plt.plot(initialCapital, 'o')
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



def LoadMostRecentValues(path):
   f = open(path, 'r')
   lines = f.readlines()
   
   param1 = int(lines[0].replace('\n', ''))
   param2 = int(lines[1].replace('\n', ''))
   param3 = int(lines[2].replace('\n', ''))
   param4 = int(lines[3].replace('\n', ''))

   return (param1, param2, param3, param4)

def SaveMostRecentValues(path, fast, slow, signal, minPositiveGain):
   f = open(path, 'w')
   f.write(str(fast) + '\n')
   f.write(str(slow) + '\n')
   f.write(str(signal) + '\n')
   f.write(str(minPositiveGain) + '\n')



def AnalizeOrders(orders):
   
   openDays = 0
   globalGain = 0
   goodTrades = 0
   badTrades = 0
   printData = False

   for order in orders:
      
      openDays += int(int(order.closeAt) - int(order.openAt))

      if(order.operationType == 'buy'):
         gain = float(float(order.closePrice) - float(order.openPrice))
      elif(order.operationType == 'sell'):
         gain = float(float(order.closePrice) - float(order.openPrice))
         gain = -gain
      
      globalGain += gain

      if(gain > 0):
         goodTrades += 1
      else:
         badTrades += 1

   if(printData == True):
      print("open days: {0}".format(openDays))
      print("global gain: {0}".format(globalGain))
      print("good trades: {0}".format(goodTrades))
      print("bad trades: {0}".format(badTrades))

   return (openDays, globalGain, goodTrades, badTrades)



'''
qui sotto per funzione con e senza processi
'''

BASE_PATH = "daUSB/schei/EURUSD/"
PATH_LOG = "log.txt"


def WriteLog(logData):
   line = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(logData.fastParam,
                                                logData.slowParam, 
                                                logData.signalParam, 
                                                logData.ema,
                                                logData.openDays, 
                                                logData.globalGain, 
                                                logData.goodTrades, 
                                                logData.badTrades,
                                                logData.numberOfBuySignals)
   f = open(dataFiles.BASE_PATH + dataFiles.PATH_LOG, "a")
   f.write(line)
   f.close()

def ComputeMACD(data, fast, slow, signal):
   #df = pd.DataFrame(data, columns = ['a'])
   #porcodio = ta.macd(data.iloc[:,1], fast = fast, slow = slow, signal = signal)
   #porcodio = np.array(porcodio)
   
   #usa questo se non parti da 0
   #df = pd.DataFrame(data, columns = ['a'])
   #porcodio = MACD(close = df.loc[:, 'a'], window_fast = fast, window_slow = slow, window_sign = signal)
   
   porcodio = MACD(close = data, window_fast = fast, window_slow = slow, window_sign = signal)
   macd = porcodio.macd()
   histogram = porcodio.macd_diff()
   sign = porcodio.macd_signal()
   
   return macd, histogram, sign

def order_openOrder(order, openPrice, openAt, orderType):
   order.openPrice = openPrice
   order.openAt = openAt
   order.operationType = orderType
   return order

def function(close, fastParam, slowParam, signalParam, ema):
   macd, histogram, signal = ComputeMACD(close, fastParam, slowParam, signalParam)
   macd = np.array(macd)
   histogram = np.array(histogram)
   signal = np.array(signal)
   length = close.shape[0]

   emaSignal = EMAIndicator(close = close, window = ema)
   emaSignal = emaSignal.ema_indicator()
   emaSignal = np.array(emaSignal)

   order = Order()
   status = Status()
   orders = []

   for i in range(0, length-1):
      if(math.isnan(macd[i]) == False and math.isnan(signal[i]) == False and math.isnan(emaSignal[i]) == False):
         status.UpdateStatus(macd[i], signal[i], histogram[i], emaSignal[i], close[i])

         buySignal = status.GenerateBuySignal()
         sellSignal = status.GenerateSellSignal()

         if(buySignal == True):
            status.numberOfBuySignals += int(1)
         
         if(sellSignal == True):
            status.numberOfSellSignals += int(1)
         
         if(status.currentlyHaveAnOrder == False):
            if(buySignal == True):
               status.currentlyHaveAnOrder = True
               order = order_openOrder(order, close[i], i, 'buy')                           
            elif(sellSignal == True):
               status.currentlyHaveAnOrder = True
               order = order_openOrder(order, close[i], i, 'sell')
         else:
            closeOrder = False

            if(order.operationType == 'buy'):
               #if(sellSignal == True):
               if(close[i] > order.openPrice + 0.001 or close[i] < order.openPrice - 0.001):
               #if(close[i] > order.openPrice + 0.01 or close[i] < order.openPrice - closeAt):
                  closeOrder = True
            elif(order.operationType == 'sell'):
               if(close[i] > order.openPrice + 0.001 or close[i] < order.openPrice - 0.001):
                  closeOrder = True

            if(closeOrder == True):
               order.closePrice = close[i]
               status.currentlyHaveAnOrder = False
               order.closeAt = i
               orders.append(deepcopy(order))
               order.Reset()
         
         status.UpdateAtTheEnd()
   
   return orders, status


