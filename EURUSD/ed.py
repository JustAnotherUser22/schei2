
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta
import pandas as pd
import math
import copy
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

PATH_DATA = "D:\script\ptr\EUR_USD Dati Storici 2022.csv"
PATH_LOG = "D:/script/ptr/log_ed_2022.txt"
PATH_LAST_PARAMETERS = "D:/script/ptr/last_parameters_2022.txt"

#############################
#  private classes
#############################

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


def createLog():
   data = LoadDataFromCSV(PATH_DATA)
   #help(ta.macd)

   close = data[:, 0]
   #close = data[0:80, 0]
   length = close.shape[0]

   #IfLogFileExistsDeleteIt(PATH_LOG)

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




import threading
import time
import datetime


#questo è più lento di un thread singolo!
#leggi
#https://blog.devgenius.io/why-is-multi-threaded-python-so-slow-f032757f72dc
#per capire il motivo



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

   

if __name__ == "__main__":
   #createLog()
   
   createLogWithProcess()
   
   #AnalyzeLog(PATH_LOG)
   