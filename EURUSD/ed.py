
#import yfinance as yf
import numpy as np
#import tensorflow
import matplotlib.pyplot as plt
import pandas_ta as ta
import pandas as pd
import math
import copy
from pathlib import Path
import os
import multiprocessing
from commons import Order
from commons import LoadDataFromCSV
from commons import Status

'''
goal:
- high global gain
- keep open position opened for as few days as possible
- high win/lose ratio

'''

#PATH_DATA = "D:\script\ptr\EUR_USD Dati Storici.csv"
#PATH_LOG = "D:/script/ptr/log_ed.txt"
#PATH_LAST_PARAMETERS = "D:/script/ptr/last_parameters.txt"
PATH_DATA = "D:\script\ptr\EUR_USD Dati Storici 2022.csv"
PATH_LOG = "D:/script/ptr/log_ed_2022.txt"
PATH_LAST_PARAMETERS = "D:/script/ptr/last_parameters_2022.txt"

#############################
#  private classes
#############################
'''
class Order:
   def __init__(self):
      self.openPrice = 0
      self.closePrice = 0
      self.openAt = 0
      self.closeAt = 0
      self.operationType = ''
   
   def Reset(self):
      self.openPrice = 0
      self.closePrice = 0
      self.openAt = 0
      self.closeAt = 0
      self.operationType = ''
'''
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
'''
class MACDParameters:
   def __init__(self, fast, slow, signal):
      self.fastParam = fast
      self.slowParam = slow
      self.signalParam = signal

class AlgoParameters:
   def __init__(self, minPositiveGain, minNegativeLoss):
      self.minPositiveGain = minPositiveGain
      self.minNegativeLoss = minNegativeLoss
      
   
#############################
#  private methods
#############################

def AnalizeOrders(orders):
   
   openDays = 0
   globalGain = 0
   goodTrades = 0
   badTrades = 0

   for order in orders:
      if(order.operationType == 'buy'):
         openDays += int(int(order.closeAt) - int(order.openAt))
         gain = float(float(order.closePrice) - float(order.openPrice))
         globalGain += gain
         if(gain > 0):
            goodTrades += 1
         else:
            badTrades += 1
      elif(order.operationType == 'sell'):
         openDays += int(int(order.closeAt) - int(order.openAt))
         gain = float(float(order.closePrice) - float(order.openPrice))
         globalGain += gain
         if(gain < 0):
            goodTrades += 1
         else:
            badTrades += 1

   #print("open days: {0}".format(openDays))
   #print("global gain: {0}".format(globalGain))
   #print("good trades: {0}".format(goodTrades))
   #print("bad trades: {0}".format(badTrades))

   return (openDays, globalGain, goodTrades, badTrades)

def WriteLog(logData):
   line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(logData.fastParam,
                                                            logData.slowParam, 
                                                            logData.signalParam, 
                                                            logData.openDays, 
                                                            logData.globalGain, 
                                                            logData.goodTrades, 
                                                            logData.badTrades,
                                                            logData.numberOfBuySignals,
                                                            logData.minPositiveGain,
                                                            logData.minNegativeLoss,
                                                            logData.initialCapital)
   f = open(PATH_LOG, "a")
   f.write(line)
   f.close()

def ComputeMACD(data, parameters):
   df = pd.DataFrame(data, columns = ['a'])
   fast = parameters.fastParam
   slow = parameters.slowParam
   signal = parameters.signalParam
   porcodio = ta.macd(df.a, fast = fast, slow = slow, signal = signal)
   porcodio = np.array(porcodio)
   return porcodio



def PrintMACDData(macdData):
   macd = macdData[:, 0]
   histogram = macdData[:, 1]
   signal = macdData[:, 2]
   #delta = histogram - macd + signal  #ok porco dio almeno questo è 0
   
   plt.plot(macd, 'r')
   #plt.plot(histogram, 'g')
   plt.plot(signal, 'b')
   #plt.plot(close)
   plt.show()

def ComputeAlgoEffectivnessWithMacdData(close, macdData, algoParameters):
   macd = macdData[:, 0]
   histogram = macdData[:, 1]
   signal = macdData[:, 2]
   length = close.shape[0]
   
   E = 0
   D = 0
   
   order = Order()
   status = Status()
   orders = []

   minPositiveGain = algoParameters.minPositiveGain
   minNegativeLoss = algoParameters.minNegativeLoss

   for i in range(0, length-1):
      if(math.isnan(macd[i]) == False and math.isnan(signal[i]) == False):
         status.UpdateStatus(macd[i], signal[i], histogram[i])

         buySignal = status.GenerateBuySignal()
         sellSignal = status.GenerateSellSignal()

         if(buySignal == True):
            status.numberOfBuySignals += int(1)

         if(status.currentlyHaveAnOrder == False):
            if(buySignal == True):
               status.currentlyHaveAnOrder = True
               order.openPrice = close[i]
               order.openAt = i
               order.operationType = 'buy'
               E += int(1)
               D -= float(close[i])
            elif(sellSignal == True):
               status.currentlyHaveAnOrder = True
               order.openPrice = close[i]
               order.openAt = i
               order.operationType = 'sell'
               E -= int(1)
               D += float(close[i])
         else:
            if(order.operationType == 'buy'):
               if(close[i] > order.openPrice + minPositiveGain or close[i] < order.openPrice - minNegativeLoss):
                  order.closePrice = close[i]
                  status.currentlyHaveAnOrder = False
                  order.closeAt = i
                  orders.append(copy.deepcopy(order))
                  order.Reset()
                  E -= int(1)
                  D += float(close[i])
            if(order.operationType == 'sell'):
               if(close[i] < order.openPrice + minPositiveGain or close[i] > order.openPrice - minNegativeLoss):
                  order.closePrice = close[i]
                  status.currentlyHaveAnOrder = False
                  order.closeAt = i
                  orders.append(copy.deepcopy(order))
                  order.Reset()
                  E += int(1)
                  D -= float(close[i])
   
         #if(status.currentlyHaveAnOrder == True):
         #   events.append(1)
         #else:
         #   events.append(0)
         
         status.UpdateAtTheEnd()
      else:
         #events.append(0)
         pass

   return orders, status

def TestAlgoInThread(name, macdData, close, minPositiveGain):
   start = datetime.datetime.now()
   print("{0} start at {1}".format(name, start))

   for minNegativeLoss in np.arange(0.0, 0.5, 0.001):

      algoParameters = AlgoParameters(minPositiveGain, minNegativeLoss)

      macd = macdData[:, 0]
      histogram = macdData[:, 1]
      signal = macdData[:, 2]
      #delta = histogram - macd + signal  #ok porco dio almeno questo è 0

      orders, status, = ComputeAlgoEffectivnessWithMacdData(close, macdData, algoParameters)
      
      openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)

   print("{0},{1},{2},{3},{4},{5}".format(name, 
                                          minPositiveGain, 
                                          minNegativeLoss, 
                                          globalGain, 
                                          E, 
                                          U))

   delta = datetime.datetime.now() - start
   print("{0} end in {1}".format(name, delta))

def TestAlgoInProcess(name, macdData, close, minPositiveGain, dict):
   start = datetime.datetime.now()
   print("{0} start at {1}".format(name, start))

   dictionaryIndex = 0

   FINAL_VALUE = 0.19 #0.5

   for minNegativeLoss in np.arange(0.0, FINAL_VALUE, 0.001):

      algoParameters = AlgoParameters(minPositiveGain, minNegativeLoss)

      macd = macdData[:, 0]
      histogram = macdData[:, 1]
      signal = macdData[:, 2]
      #delta = histogram - macd + signal  #ok porco dio almeno questo è 0

      orders, status = ComputeAlgoEffectivnessWithMacdData(close, macdData, algoParameters)
      
      openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)

      initialCapital = 0

      if(globalGain > 0):
         stringa = "{0},{1},{2},{3},{4},{5},{6},{7}".format(openDays, 
                                                globalGain,
                                                goodTrades,
                                                badTrades,
                                                status.numberOfBuySignals,
                                                minPositiveGain, 
                                                minNegativeLoss, 
                                                initialCapital)
      
         dict[dictionaryIndex] = stringa
         dictionaryIndex += int(1)

      '''
      if(globalGain > 0):
         stringa = "{0},{1},{2},{3},{4},{5}".format(name, 
                                          minPositiveGain, 
                                          minNegativeLoss, 
                                          globalGain, 
                                          E, 
                                          U)
      '''

   #print(stringa)

   delta = datetime.datetime.now() - start
   print("{0} end in {1}".format(name, delta))



#############################
#  public methods
#############################
def printGraphFromOrdersList(orders):
   graph = []
   total = 0

   for order in orders:
      if(order.openAt != 0):
         total -= float(order.openPrice)
         graph.append(total)
      if(order.closeAt != 0):
         total += float(order.closePrice)
         graph.append(total)

   plt.plot(graph)

def createLog():
   data = LoadDataFromCSV(PATH_DATA)
   #help(ta.macd)

   close = data[:, 0]
   #close = data[0:80, 0]
   length = close.shape[0]

   #IfLogFileExistsDeleteIt(PATH_LOG)

   events = []

   for fastParam in range(1, 25):
      for slowParam in range (fastParam + 1, 40):
         for signalParam in range (9, 15):

            parameters = MACDParameters(fastParam, slowParam, signalParam)
            macdData = ComputeMACD(close, parameters)

            for minPositiveGain in np.arange(0.0, 0.5, 0.001):
               for minNegativeLoss in np.arange(0.0, 0.5, 0.001):
            
                  #fastParam = 2
                  #slowParam = 22
                  #signalParam = 4
                  #minPositiveGain = 0.1
                  #minNegativeLoss = 1
                  #initialCapital = 1000

                  #parameters = MACDParameters(fastParam, slowParam, signalParam)
                  #macdData = ComputeMACD(close, parameters)

                  algoParameters = AlgoParameters(minPositiveGain, minNegativeLoss)

                  macd = macdData[:, 0]
                  histogram = macdData[:, 1]
                  signal = macdData[:, 2]
                  #delta = histogram - macd + signal  #ok porco dio almeno questo è 0
               
                  #PrintMACDData(macdData)
                  
                  orders, status = ComputeAlgoEffectivnessWithMacdData(close, macdData, algoParameters)
                  
                  openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)

                  if(globalGain > 0):
                     print("{0},{1},{2},{3},{4},{5},{6},{7}".format(parameters.fastParam, 
                                                               parameters.slowParam, 
                                                               parameters.signalParam, 
                                                               minPositiveGain, 
                                                               minNegativeLoss, 
                                                               globalGain, 
                                                               E, 
                                                               U))

                     logData = LogData()
                     logData.openDays = openDays
                     logData.globalGain = globalGain
                     logData.goodTrades = goodTrades
                     logData.badTrades = badTrades
                     logData.fastParam = parameters.fastParam
                     logData.slowParam = parameters.slowParam
                     logData.signalParam = parameters.signalParam
                     logData.minPositiveGain = minPositiveGain
                     logData.minNegativeLoss = minNegativeLoss
                     logData.numberOfBuySignals = status.numberOfBuySignals
                     logData.initialCapital = 0
                     WriteLog(logData)

def LoadLog():
   f = open(PATH_LOG, "r")
   lines = f.readlines()
   counter = 0

   data = []

   for line in lines:
      log = LogData()
      dataInLine = line.split(',')
      log.fastParam = dataInLine[0]
      log.slowParam = dataInLine[1]
      log.signalParam = dataInLine[2]
      log.openDays = dataInLine[3]
      log.globalGain = float(dataInLine[4])
      log.goodTrades = dataInLine[5]
      log.badTrades = dataInLine[6]
      log.numberOfBuySignals = dataInLine[7]
      log.minPositiveGain = dataInLine[8]
      log.minNegativeLoss = dataInLine[9]
      log.initialCapital = float(dataInLine[10])
      log.winRate = float(log.goodTrades) / (float(log.goodTrades) + float(log.badTrades))
      data.append(copy.deepcopy(log))
      counter += int(1)

   #data.sort(key = lambda x: x.globalGain, reverse = True)

   positiveGain = [i for i in data if i.globalGain > 0]
   goodWr = [i for i in positiveGain if i.winRate > 0.5]
   goodWr.sort(key = lambda x: x.winRate, reverse = True)

   print("done")

def PrintGapBetweenClosAndOpenOfNextDay():
   data = LoadDataFromCSV(PATH_DATA)
   #help(ta.macd)

   close = data[:, 0]
   open = data[:, 1]
   
   length = close.shape[0]

   open = open.pop()
   close = close.pop(length - 1)
   
   delta = close - open

   plt.plot(delta)

def WithThreads():
   import threading

   data = LoadDataFromCSV(PATH_DATA)
   close = data[:, 0]
   
   fastParam = 2
   slowParam = 22
   signalParam = 4
   
   parameters = MACDParameters(fastParam, slowParam, signalParam)
   macdData = ComputeMACD(close, parameters)

   minPositiveGain_t1 = 0.02
   minPositiveGain_t2 = 0.03
   
   threading.Thread( target = TestAlgoInThread, args = ("thread-1", macdData, close, minPositiveGain_t1 ) ).start()
   threading.Thread( target = TestAlgoInThread, args = ("thread-2", macdData, close, minPositiveGain_t2 ) ).start()

import threading
import time
import datetime

class myThread (threading.Thread):
   def __init__(self, threadID, name, macdData, close, minPositiveGain):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.startTime = 0
      self.stopTime = 0
      self.log = 0
      self.macdData = macdData
      self.close = close
      self.minPositiveGain = minPositiveGain

   def run(self):
      print( "Starting " + self.name)
      self.startTime = datetime.datetime.now()
      self.TestAlgoInThread()
      self.stopTime = datetime.datetime.now()
      delta = self.stopTime - self.startTime
      print("Exiting {0}, time = {1}".format(self.name, str(delta)))      
   
   def TestAlgoInThread(self):   
      
      for minNegativeLoss in np.arange(0.0, 0.5, 0.001):

         algoParameters = AlgoParameters(self.minPositiveGain, minNegativeLoss)

         macd = self.macdData[:, 0]
         histogram = self.macdData[:, 1]
         signal = self.macdData[:, 2]
         #delta = histogram - macd + signal  #ok porco dio almeno questo è 0

         orders, status = ComputeAlgoEffectivnessWithMacdData(self.close, self.macdData, algoParameters)
         
         openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)
      '''
      print("{0},{1},{2},{3},{4}".format(self.minPositiveGain, 
                                          minNegativeLoss, 
                                          globalGain, 
                                          E, 
                                          U))
      '''

   def reset(self):
      self.startTime = 0
      self.stopTime = 0
      self.log = 0

class processWrapper:
   def __init__(self, name, macdData, close, minPositiveGain):
      self.localProcess = None
      self.name = name
      self.macdData = macdData
      self.close = close
      self.isRunning = False

   def startProcess(self):
      if(self.isRunning == False):
         self.isRunning = True
         manager = multiprocessing.Manager()
         return_dict = manager.dict()
         
         minPositiveGain_t1 = minPositiveGain
         
         self.localProcess = multiprocessing.Process(target = TestAlgoInProcess, args = (self.name, self.macdData, self.close, minPositiveGain_t1, return_dict))

         self.localProcess.start()

   def waitEndProcess(self):
      self.localProcess.join()

#questo è più lento di un thread singolo!
#leggi
#https://blog.devgenius.io/why-is-multi-threaded-python-so-slow-f032757f72dc
#per capire il motivo
def WithThreadsAndClass():
   data = LoadDataFromCSV(PATH_DATA)
   close = data[:, 0]
   
   fastParam = 2
   slowParam = 22
   signalParam = 4
   
   parameters = MACDParameters(fastParam, slowParam, signalParam)
   macdData = ComputeMACD(close, parameters)

   minPositiveGain_t1 = 0.02
   minPositiveGain_t2 = 0.03
   
   # Create new threads
   thread1 = myThread(1, "Thread-1", macdData, close, minPositiveGain_t1)
   thread2 = myThread(2, "Thread-2", macdData, close, minPositiveGain_t2)
   thread3 = myThread(3, "Thread-3", macdData, close, minPositiveGain_t2)


   # Start new Threads
   thread1.start()
   thread2.start()
   thread3.start()

   print( "Exiting Main Thread")

   thread1.join()
   thread2.join()
   thread3.join()

   #print("data from t1 " + str(thread1.counter))
   #print("data from t2 " + str(thread2.counter))

   thread1.reset()
   thread2.reset()

def WithProcess():
   data = LoadDataFromCSV(PATH_DATA)
   close = data[:, 0]
   
   fastParam = 2
   slowParam = 22
   signalParam = 4
   
   parameters = MACDParameters(fastParam, slowParam, signalParam)
   macdData = ComputeMACD(close, parameters)

   minPositiveGain_t1 = 0.02
   minPositiveGain_t2 = 0.03
   minPositiveGain_t3 = 0.04
   minPositiveGain_t4 = 0.05

   manager = multiprocessing.Manager()
   return_dict_1 = manager.dict()
   return_dict_2 = manager.dict()
   return_dict_3 = manager.dict()
   return_dict_4 = manager.dict()
   
   p1 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p1", macdData, close, minPositiveGain_t1, return_dict_1))
   p2 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p2", macdData, close, minPositiveGain_t2, return_dict_2))
   p3 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p3", macdData, close, minPositiveGain_t3, return_dict_3))
   p4 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p4", macdData, close, minPositiveGain_t4, return_dict_4))

   p1.start()
   #p2.start()
   #p3.start()
   #p4.start()

   p1.join()
   #p2.join()
   #p3.join()
   #p4.join()

   print(return_dict_1.values())
   for entry in return_dict_1.values():
      print(entry)
   #print(return_dict_1.values())
   #print(return_dict_2.values())
   #print(return_dict_3.values())
   #print(return_dict_4.values())

def createLogWithProcess():
   data = LoadDataFromCSV(PATH_DATA)
   #help(ta.macd)

   close = data[:, 0]
   #close = data[0:80, 0]
   length = close.shape[0]

   #IfLogFileExistsDeleteIt(PATH_LOG)

   events = []

   needToLoadMostRecentValues = True

   #NOTA: la lenta deve sempre essere fatta su più campioni rispetto la veloce!!

   FAST_PARAMETER_MIN_VALUE = 1
   FAST_PARAMETER_MAX_VALUE = 25
   SLOW_PARAMETER_MIN_VALUE = 1
   SLOW_PARAMETER_MAX_VALUE = 40
   SIGNAL_PARAMETER_MIN_VALUE = 1
   SIGNAL_PARAMETER_MAX_VALUE = 16
   POSITIVE_GAIN_MIN_VALUE = 0.001
   POSITIVE_GAIN_MAX_VALUE = 0.19 #0.5

   fastParam = FAST_PARAMETER_MIN_VALUE
   slowParam = SLOW_PARAMETER_MIN_VALUE
   signalParam = SIGNAL_PARAMETER_MIN_VALUE
   minPositiveGain = POSITIVE_GAIN_MIN_VALUE
   mostRecentefastParam, mostRecenteslowParam, mostRecentesignalParam, mostRecentMinPositiveGain = LoadMostRecentValues(PATH_LAST_PARAMETERS)
               
   while(fastParam < FAST_PARAMETER_MAX_VALUE):
      slowParam = fastParam
      while(slowParam < SLOW_PARAMETER_MAX_VALUE):
         signalParam = SIGNAL_PARAMETER_MIN_VALUE
         while(signalParam < SIGNAL_PARAMETER_MAX_VALUE):

            if(needToLoadMostRecentValues == True):
               fastParam = mostRecentefastParam
               slowParam = mostRecenteslowParam
               signalParam = mostRecentesignalParam

            #fai cose
            parameters = MACDParameters(fastParam, slowParam, signalParam)
            macdData = ComputeMACD(close, parameters)

            if(needToLoadMostRecentValues == True):
               needToLoadMostRecentValues = False
               minPositiveGain = mostRecentMinPositiveGain
            else:
               minPositiveGain = POSITIVE_GAIN_MIN_VALUE

            while(minPositiveGain < POSITIVE_GAIN_MAX_VALUE):
               start = datetime.datetime.now()
               print("run start at {0}".format(start))
               
               macd = macdData[:, 0]
               histogram = macdData[:, 1]
               signal = macdData[:, 2]
               #delta = histogram - macd + signal  #ok porco dio almeno questo è 0
               
               manager = multiprocessing.Manager()
               return_dict_1 = manager.dict()
               return_dict_2 = manager.dict()
               return_dict_3 = manager.dict()
               return_dict_4 = manager.dict()
               return_dict_5 = manager.dict()

               minPositiveGain_t1 = minPositiveGain
               minPositiveGain_t2 = minPositiveGain + 0.001
               minPositiveGain_t3 = minPositiveGain + 0.002
               minPositiveGain_t4 = minPositiveGain + 0.003
               minPositiveGain_t5 = minPositiveGain + 0.004

               print(minPositiveGain_t1)

               p1 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p1", macdData, close, minPositiveGain_t1, return_dict_1))
               p2 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p2", macdData, close, minPositiveGain_t2, return_dict_2))
               p3 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p3", macdData, close, minPositiveGain_t3, return_dict_3))
               p4 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p4", macdData, close, minPositiveGain_t4, return_dict_4))
               p5 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p5", macdData, close, minPositiveGain_t5, return_dict_5))

               p1.start()
               p2.start()
               p3.start()
               p4.start()
               p5.start()

               p1.join()
               p2.join()
               p3.join()
               p4.join()
               p5.join()

               allDict = []
               for entry in return_dict_1.values():
                  allDict.append(entry)
               for entry in return_dict_2.values():
                  allDict.append(entry)
               for entry in return_dict_3.values():
                  allDict.append(entry)
               for entry in return_dict_4.values():
                  allDict.append(entry)
               for entry in return_dict_5.values():
                  allDict.append(entry)

               for entry in allDict:
                  #print(entry)
                  line = "{0},{1},{2},".format(parameters.fastParam, parameters.slowParam, parameters.signalParam)
                  line += str(entry)
                  line += '\n'
                  #print(line)

                  f = open(PATH_LOG, "a")
                  f.write(line)
                  f.close()

               SaveMostRecentValues(PATH_LAST_PARAMETERS, fastParam, slowParam, signalParam, minPositiveGain)

               delta = datetime.datetime.now() - start
               print("run ends in {0}".format(delta))
 
               
               minPositiveGain += 0.005
            signalParam += 1
         slowParam += 1
      fastParam += 1

   '''
   for fastParam in range(1, 25):
      #for slowParam in range (fastParam + 1, 40):
      for slowParam in range (6, 40):
         for signalParam in range (11, 16):

            parameters = MACDParameters(fastParam, slowParam, signalParam)
            macdData = ComputeMACD(close, parameters)
            
            for minPositiveGain in np.arange(0.25, 0.5, 0.005):
               #for minNegativeLoss in np.arange(0.0, 0.5, 0.001):
            
               #fastParam = 2
               #slowParam = 22
               #signalParam = 4
               #minPositiveGain = 0.1
               #minNegativeLoss = 1
               #initialCapital = 1000

               #algoParameters = AlgoParameters(minPositiveGain, minNegativeLoss)

               macd = macdData[:, 0]
               histogram = macdData[:, 1]
               signal = macdData[:, 2]
               #delta = histogram - macd + signal  #ok porco dio almeno questo è 0

               manager = multiprocessing.Manager()
               return_dict_1 = manager.dict()
               return_dict_2 = manager.dict()
               return_dict_3 = manager.dict()
               return_dict_4 = manager.dict()
               return_dict_5 = manager.dict()

               minPositiveGain_t1 = minPositiveGain
               minPositiveGain_t2 = minPositiveGain + 0.001
               minPositiveGain_t3 = minPositiveGain + 0.002
               minPositiveGain_t4 = minPositiveGain + 0.003
               minPositiveGain_t5 = minPositiveGain + 0.004

               print(minPositiveGain_t1)

               p1 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p1", macdData, close, minPositiveGain_t1, return_dict_1))
               p2 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p2", macdData, close, minPositiveGain_t2, return_dict_2))
               p3 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p3", macdData, close, minPositiveGain_t3, return_dict_3))
               p4 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p4", macdData, close, minPositiveGain_t4, return_dict_4))
               p5 = multiprocessing.Process(target = TestAlgoInProcess, args = ("p5", macdData, close, minPositiveGain_t5, return_dict_5))

               p1.start()
               p2.start()
               p3.start()
               p4.start()
               p5.start()

               p1.join()
               p2.join()
               p3.join()
               p4.join()
               p5.join()

               allDict = []
               for entry in return_dict_1.values():
                  allDict.append(entry)
               for entry in return_dict_2.values():
                  allDict.append(entry)
               for entry in return_dict_3.values():
                  allDict.append(entry)
               for entry in return_dict_4.values():
                  allDict.append(entry)
               for entry in return_dict_5.values():
                  allDict.append(entry)
               
               for entry in allDict:
                  #print(entry)
                  line = "{0},{1},{2},".format(parameters.fastParam, parameters.slowParam, parameters.signalParam)
                  line += str(entry)
                  line += '\n'
                  #print(line)

                  f = open(PATH_LOG, "a")
                  f.write(line)
                  f.close()
   '''

   '''
               line = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(parameters.fastParam,
                                                         parameters.slowParam, 
                                                         parameters.signalParam, 
                                                         openDays, 
                                                         globalGain, 
                                                         goodTrades, 
                                                         badTrades,
                                                         status.numberOfBuySignals,
                                                         status.minPositiveGain,
                                                         minNegativeLoss,
                                                         status.initialCapital)
   '''

def AnalyzeData():
   data = LoadDataFromCSV(PATH_DATA)
   close = data[:, 0]

   dataDimensions = np.shape(close)
   minimumValue = np.amin(close)
   maximumValue = np.amax(close)

   print("data dimensions: {0}".format(dataDimensions))
   print("minimum value: {0}".format(minimumValue))
   print("maximum value: {0}".format(maximumValue))

if __name__ == "__main__":
   #createLog()
   #WithThreads()
   #WithThreadsAndClass()
   #WithProcess()
   
   createLogWithProcess()
   #AnalyzeData()

   #AnalyzeLog(PATH_LOG)
   #LoadLog()
   #PrintGapBetweenClosAndOpenOfNextDay()