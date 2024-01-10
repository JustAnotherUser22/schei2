import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta
import pandas as pd
import math
from copy import deepcopy
from pathlib import Path
import os
from ta.trend import MACD
from ta.trend import EMAIndicator
from ta.volatility import BollingerBands
from pylab import *
from commons import Order
from commons import GetValueFromLines
from commons import LoadMostRecentValues
from commons import LogData
from commons import SaveMostRecentValues
from commons import AnalyzeLog
from commons import Status
from commons import AnalizeOrders
import multiprocessing


'''
goal:
- high global gain
- keep open position opened for as few days as possible
- high win/lose ratio

'''


BASE_PATH = "daUSB/schei/EURUSD/"
PATH_LOG = "log.txt"
PATH_LAST_PARAMETERS = "last_parameters_macd.txt"
PATH_TEST_LAST_PARAMETERS = "test_last_parameters.txt"

#NOTA: la lenta deve sempre essere fatta su più campioni rispetto la veloce!!
FAST_PARAMETER_MIN_VALUE = 1
FAST_PARAMETER_MAX_VALUE = 25
SLOW_PARAMETER_MIN_VALUE = 1
SLOW_PARAMETER_MAX_VALUE = 40
SIGNAL_PARAMETER_MIN_VALUE = 1
SIGNAL_PARAMETER_MAX_VALUE = 30
EMA_PARAMETER_MAX_VALUE = 500
   

#############################
#  private methods
#############################

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
   f = open(BASE_PATH + PATH_LOG, "a")
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


#############################
#  public methods
#############################

      
def getNextParameters():
   fastParam, slowParam, signalParam, ema = LoadMostRecentValues(BASE_PATH + PATH_LAST_PARAMETERS)

   terminate = False

   if(fastParam == FAST_PARAMETER_MAX_VALUE and
      slowParam == SLOW_PARAMETER_MAX_VALUE and
      signalParam == SIGNAL_PARAMETER_MAX_VALUE and
      ema == EMA_PARAMETER_MAX_VALUE):
      terminate = True

   if(ema < EMA_PARAMETER_MAX_VALUE):
      ema += int(1)
   elif(signalParam < SIGNAL_PARAMETER_MAX_VALUE):
      ema = 1
      signalParam += int(1)
   elif(slowParam < SLOW_PARAMETER_MAX_VALUE):
      ema = 1
      slowParam += int(1)
      signalParam = SIGNAL_PARAMETER_MIN_VALUE
   elif(fastParam < FAST_PARAMETER_MAX_VALUE):
      ema = 1
      fastParam += int(1)
      slowParam = fastParam + 1
      signalParam = SIGNAL_PARAMETER_MIN_VALUE

   SaveMostRecentValues(BASE_PATH + PATH_LAST_PARAMETERS, fastParam, slowParam, signalParam, ema)

   values = {
      "slow": slowParam,
      "fast": fastParam,
      "signal": signalParam,
      "ema": ema,
      "terminate": terminate
   }

   return values

def withProcesses():
   
   numberOfCores = multiprocessing.cpu_count() - int(3)

   mutex = {
      "mutexLoadParameters": multiprocessing.Lock(),
      "mutexLoadData": multiprocessing.Lock(),
      "mutexWriteResults": multiprocessing.Lock(),
   }


   processList = []
   for i in range(numberOfCores):
      name = 'p' + str(i)
      p = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, name))
      processList.append(p)
      processList[i].start()

   for i in range(numberOfCores):
      processList[i].join()



def functionToCallInProcess(mutex, name):
   mutex["mutexLoadData"].acquire()
   #data = pd.read_csv(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_window_100.csv")
   data = pd.read_csv(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv")
   close = data.iloc[:,1]
   mutex["mutexLoadData"].release()
   
   keepGoing = True

   while(keepGoing):
      
      mutex["mutexLoadParameters"].acquire()
      #print(name + " lock")
      parameters = getNextParameters()
      #print(name + " unlock")
      mutex["mutexLoadParameters"].release()

      keepGoing = not parameters["terminate"]
      if(keepGoing):
         fast = parameters["fast"]
         slow = parameters["slow"]
         signal = parameters["signal"]
         ema = parameters["ema"]
         orders, status = function(close, fast, slow, signal, ema)
         openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)

         logData = LogData()
         logData.openDays = openDays
         logData.globalGain = "{:.6f}".format(round(globalGain, 6))
         logData.goodTrades = goodTrades
         logData.badTrades = badTrades
         logData.fastParam = fast
         logData.slowParam = slow
         logData.signalParam = signal
         logData.ema = ema
         #logData.closeAt = closeAt
         logData.numberOfBuySignals = status.numberOfBuySignals

         if(globalGain > 0):
            mutex["mutexWriteResults"].acquire()
            WriteLog(logData)
            mutex["mutexWriteResults"].release()



if __name__ == "__main__":
   withProcesses()
   